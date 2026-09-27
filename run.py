#!/usr/bin/env python3

import argparse
import hmac
import json
import os
import platform
import re
import shlex
import signal
import socket
import shutil
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"
BACKEND_DIR = ROOT / "backend"
COMPOSE_FILE = BACKEND_DIR / "docker-compose.yml"
BACKEND_ENV_FILE = BACKEND_DIR / ".env"
BACKEND_ENV_EXAMPLE_FILE = BACKEND_DIR / ".env.example"
FRONTEND_PACKAGE_FILE = FRONTEND_DIR / "package.json"
FRONTEND_LOCK_FILE = FRONTEND_DIR / "package-lock.json"
RUN_STATE_DIR = ROOT / ".run-state"

BACKEND_COMMAND = ["gradlew.bat", "bootRun"]
BACKEND_COMMAND_UNIX = ["./gradlew", "bootRun"]
SERVICE_COMMANDS = {
    "backend": (BACKEND_COMMAND, BACKEND_COMMAND_UNIX, BACKEND_DIR),
    "frontend": (None, None, FRONTEND_DIR),
}


# ============================================================
# Helpers
# ============================================================

def print_header():
    print()
    print("=" * 60)
    print("              LANCEMENT DU PROJET")
    print("=" * 60)
    print(f"Racine : {ROOT}")
    print()


def choose_os():
    detected = platform.system()

    print("Système détecté :", detected)
    print()
    print("1. macOS")
    print("2. Windows")
    print("3. Linux")
    print()

    choice = input(
        "Choisis ton système [Entrée = détection automatique] : "
    ).strip()

    if not choice:
        if detected == "Darwin":
            return "mac"
        if detected == "Windows":
            return "windows"
        return "linux"

    mapping = {
        "1": "mac",
        "2": "windows",
        "3": "linux",
    }

    if choice not in mapping:
        print("❌ Choix invalide.")
        raise SystemExit(1)

    return mapping[choice]


def fail(message):
    print(f"❌ {message}")
    raise SystemExit(1)


def choose_action():
    print("1. Lancer le projet")
    print("2. Arrêter le projet")
    choice = input("Choisis une action [1] : ").strip()
    if choice in ("", "1"):
        return "start"
    if choice == "2":
        return "stop"
    fail("Choix invalide.")


def command_exists(command):
    return shutil.which(command) is not None


def run_check(command, cwd=None):
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        fail(f"Commande introuvable ou impossible à exécuter : {command[0]}")


def npm_executable(os_name):
    return "npm.cmd" if os_name == "windows" else "npm"


def check_project_structure():
    missing = [
        path
        for path in (FRONTEND_DIR, BACKEND_DIR, COMPOSE_FILE)
        if not path.exists()
    ]

    if missing:
        print("❌ Éléments du projet introuvables :")
        for path in missing:
            print(f"   - {path}")
        fail("Vérifie la structure du projet et les chemins dans run.py.")


def check_java():
    if not command_exists("java"):
        fail("Java 21 est requis, mais la commande « java » est introuvable.")

    result = run_check(["java", "-version"])
    version_output = f"{result.stdout}\n{result.stderr}"
    match = re.search(r'version\s+"?(\d+)', version_output, re.IGNORECASE)

    if result.returncode != 0 or not match:
        fail("Impossible de déterminer la version de Java avec « java -version ».")

    if int(match.group(1)) < 21:
        fail(
            "Java 21 est requis. Version détectée : "
            f"{match.group(1)}. Vérifie JAVA_HOME et le PATH."
        )

    print("✓ Java 21")


def check_node(os_name):
    if not command_exists("node"):
        fail("Node.js est requis, mais la commande « node » est introuvable.")

    result = run_check(["node", "--version"])
    match = re.search(r"v?(\d+)\.(\d+)\.(\d+)", result.stdout)

    if result.returncode != 0 or not match:
        fail("Impossible de déterminer la version de Node.js.")

    version = tuple(int(part) for part in match.groups())
    supported = (
        version[0] == 22 and version >= (22, 18, 0)
    ) or version >= (24, 12, 0)

    if not supported:
        fail(
            "Node.js ^22.18.0 ou >=24.12.0 est requis. "
            f"Version détectée : {result.stdout.strip()}."
        )

    npm = npm_executable(os_name)
    if not command_exists(npm):
        fail("npm est requis, mais la commande « npm » est introuvable.")

    npm_result = run_check([npm, "--version"])
    if npm_result.returncode != 0:
        fail("npm est installé mais ne peut pas être exécuté.")

    print(f"✓ Node.js {result.stdout.strip()} et npm {npm_result.stdout.strip()}")


def check_backend_environment():
    if not BACKEND_ENV_FILE.is_file():
        fail(
            f"Fichier requis introuvable : {BACKEND_ENV_FILE}\n"
            "Crée-le à partir de backend/.env.example, puis configure "
            "notamment JWT_SECRET."
        )

    if not BACKEND_ENV_EXAMPLE_FILE.is_file():
        fail(f"Fichier d'exemple introuvable : {BACKEND_ENV_EXAMPLE_FILE}")

    environment = {}
    for line in BACKEND_ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        environment[key.strip()] = value

    required = ("POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "JWT_SECRET")
    missing = [key for key in required if not environment.get(key)]
    if missing:
        fail(
            "Variables absentes ou vides dans backend/.env : "
            + ", ".join(missing)
        )

    jwt_secret = environment["JWT_SECRET"]
    if (
        jwt_secret == "replace-with-a-random-secret-at-least-32-bytes"
        or len(jwt_secret.encode("utf-8")) < 32
    ):
        fail(
            "JWT_SECRET doit être une clé locale non-exemple d'au moins "
            "32 octets (UTF-8)."
        )

    print("✓ Variables backend présentes et JWT_SECRET valide")


def check_dependencies(os_name):
    print("Vérification des dépendances...")

    check_java()
    check_node(os_name)

    if not command_exists("docker"):
        fail("Docker n'est pas disponible dans le PATH.")

    compose_version = run_check(["docker", "compose", "version"])
    if compose_version.returncode != 0:
        fail("Docker Compose v2 est indisponible. Vérifie l'installation de Docker.")

    docker_status = run_check(["docker", "info", "--format", "{{.ServerVersion}}"])
    if docker_status.returncode != 0:
        fail("Le moteur Docker ne répond pas. Démarre Docker Desktop puis réessaie.")

    gradle_wrapper = BACKEND_DIR / (
        "gradlew.bat" if os_name == "windows" else "gradlew"
    )
    if not gradle_wrapper.is_file():
        fail(f"Gradle Wrapper introuvable : {gradle_wrapper}")

    check_backend_environment()

    if not FRONTEND_PACKAGE_FILE.is_file() or not FRONTEND_LOCK_FILE.is_file():
        fail("package.json ou package-lock.json est introuvable dans frontend/.")

    if not (FRONTEND_DIR / "node_modules" / "vite").is_dir():
        fail(
            "Les dépendances frontend ne sont pas installées.\n"
            "Exécute « npm ci » dans le dossier frontend, puis relance le script."
        )

    compose_check = run_check(
        ["docker", "compose", "-f", COMPOSE_FILE.name, "config", "--quiet"],
        cwd=BACKEND_DIR,
    )
    if compose_check.returncode != 0:
        details = (compose_check.stderr or compose_check.stdout).strip()
        fail(f"La configuration Docker Compose est invalide.\n{details}")

    print("✓ Docker et Docker Compose")
    print("✓ Gradle Wrapper")
    print("✓ Configuration Docker Compose")
    print("✓ Dépendances frontend installées")
    print()


# ============================================================
# Docker
# ============================================================

def start_docker():
    print("🐳 Démarrage de Docker Compose...")

    container_name = "office-postgres"
    containers = run_check(
        ["docker", "container", "ls", "--all", "--format", "{{.Names}}"]
    )
    if containers.returncode != 0:
        details = (containers.stderr or containers.stdout).strip()
        fail(f"Impossible de vérifier les conteneurs Docker.\n{details}")

    if container_name in containers.stdout.splitlines():
        inspected = run_check(
            ["docker", "container", "inspect", "--format", "{{.State.Status}}", container_name]
        )
        if inspected.returncode != 0:
            details = (inspected.stderr or inspected.stdout).strip()
            fail(f"Impossible de vérifier le conteneur {container_name}.\n{details}")

        if inspected.stdout.strip() == "running":
            print(f"✓ Conteneur PostgreSQL existant réutilisé : {container_name}")
            print()
            return

        result = subprocess.run(
            ["docker", "container", "start", container_name],
            check=False,
        )
        if result.returncode != 0:
            fail(f"Impossible de démarrer le conteneur existant {container_name}.")

        print(f"✓ Conteneur PostgreSQL existant démarré : {container_name}")
        print()
        return

    result = subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE.name, "up", "-d"],
        cwd=BACKEND_DIR,
        check=False,
    )

    if result.returncode != 0:
        fail("Impossible de démarrer Docker Compose.")

    print("✓ Docker Compose démarré")
    print()


def service_state_file(service):
    return RUN_STATE_DIR / f"{service}.json"


def run_service(service):
    if service not in SERVICE_COMMANDS:
        fail(f"Service inconnu : {service}")

    _, _, cwd = SERVICE_COMMANDS[service]
    os_name = "windows" if os.name == "nt" else "unix"
    if service == "backend":
        command = BACKEND_COMMAND if os_name == "windows" else BACKEND_COMMAND_UNIX
    else:
        command = [npm_executable("windows" if os_name == "windows" else "unix"), "run", "dev"]

    RUN_STATE_DIR.mkdir(exist_ok=True)
    token = uuid.uuid4().hex
    stop_requested = threading.Event()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    server.settimeout(0.5)
    port = server.getsockname()[1]
    state_file = service_state_file(service)
    temporary_state_file = state_file.with_suffix(".tmp")

    def listen_for_stop():
        while not stop_requested.is_set():
            try:
                connection, _ = server.accept()
            except socket.timeout:
                continue
            except OSError:
                return

            with connection:
                received = connection.recv(256).decode("ascii", errors="replace")
                if hmac.compare_digest(received, token):
                    connection.sendall(b"OK")
                    stop_requested.set()
                else:
                    connection.sendall(b"DENIED")

    worker = threading.Thread(target=listen_for_stop, daemon=True)
    process = None
    try:
        temporary_state_file.write_text(
            json.dumps({"port": port, "token": token}),
            encoding="utf-8",
        )
        temporary_state_file.replace(state_file)
        worker.start()

        if os.name == "nt":
            process = subprocess.Popen(
                subprocess.list2cmdline(command),
                cwd=cwd,
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
        else:
            process = subprocess.Popen(command, cwd=cwd, start_new_session=True)

        while process.poll() is None and not stop_requested.wait(0.25):
            pass

        if process.poll() is None:
            print(f"\nArrêt gracieux du service {service}...")
            if os.name == "nt":
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(process.pid, signal.SIGINT)

            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                print(f"Le service {service} ne répond pas, arrêt forcé...")
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                        check=False,
                        capture_output=True,
                    )
                else:
                    os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if os.name == "nt":
                        process.kill()
                    else:
                        os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
        return process.returncode or 0
    finally:
        stop_requested.set()
        server.close()
        worker.join(timeout=1)
        for path in (state_file, temporary_state_file):
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def stop_service(service):
    state_file = service_state_file(service)
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
        port = int(state["port"])
        token = state["token"]
    except FileNotFoundError:
        print(f"• Aucun service {service} lancé par run.py.")
        return True
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"⚠️ État du service {service} illisible : {error}")
        return False

    if not isinstance(token, str) or not 1 <= port <= 65535:
        print(f"⚠️ État du service {service} invalide.")
        return False

    try:
        with socket.create_connection(("127.0.0.1", port), timeout=3) as connection:
            connection.sendall(token.encode("ascii"))
            response = connection.recv(16)
    except OSError as error:
        print(f"⚠️ Impossible de contacter le service {service} : {error}")
        return False

    if response != b"OK":
        print(f"⚠️ Le service {service} a refusé la demande d'arrêt.")
        return False

    deadline = time.monotonic() + 20
    while state_file.exists() and time.monotonic() < deadline:
        time.sleep(0.25)

    if state_file.exists():
        print(f"⚠️ Le service {service} n'a pas terminé dans le délai prévu.")
        return False

    print(f"✓ Service {service} arrêté proprement")
    return True


def stop_project():
    print("🛑 Arrêt des services applicatifs...")
    services_stopped = True
    for service in ("frontend", "backend"):
        if not stop_service(service):
            services_stopped = False

    if not command_exists("docker"):
        print("⚠️ Docker est introuvable ; PostgreSQL n'a pas été arrêté.")
        return False

    docker_result = run_check(
        ["docker", "compose", "-f", COMPOSE_FILE.name, "stop"],
        cwd=BACKEND_DIR,
    )
    if docker_result.returncode != 0:
        details = (docker_result.stderr or docker_result.stdout).strip()
        print(f"❌ Impossible d'arrêter Docker Compose.\n{details}")
        return False

    postgres_status = run_check(
        ["docker", "container", "inspect", "--format", "{{.State.Status}}", "office-postgres"]
    )
    if postgres_status.returncode == 0 and postgres_status.stdout.strip() == "running":
        print("• Conteneur office-postgres préexistant laissé actif.")
    else:
        print("✓ PostgreSQL arrêté (conteneur et données conservés)")
    return services_stopped


# ============================================================
# Ouverture des terminaux
# ============================================================

def start_windows_terminal(command, cwd, title):
    terminal_command = [
        "wt.exe",
        "-w",
        "0",
        "new-tab",
        "--title",
        title,
        "--startingDirectory",
        str(cwd),
        "cmd.exe",
        "/k",
        subprocess.list2cmdline(command),
    ]
    subprocess.Popen(terminal_command, cwd=cwd)


def start_windows_console(command, cwd, title):
    subprocess.Popen(
        ["cmd.exe", "/k", f"title {title} && {subprocess.list2cmdline(command)}"],
        cwd=cwd,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )


def apple_script_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def start_mac_terminal(command, cwd, title):
    shell_command = f"cd {shlex.quote(str(cwd))} && {shlex.join(command)}"
    applescript = (
        'tell application "iTerm"\n'
        "    activate\n"
        "    if (count of windows) is 0 then\n"
        "        set terminalWindow to (create window with default profile)\n"
        "    else\n"
        "        set terminalWindow to current window\n"
        "        tell terminalWindow to create tab with default profile\n"
        "    end if\n"
        f"    tell current session of terminalWindow to set name to {apple_script_string(title)}\n"
        f"    tell current session of terminalWindow to write text {apple_script_string(shell_command)}\n"
        "end tell"
    )
    result = run_check(["osascript", "-e", applescript])
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        fail(f"Impossible d'ouvrir un onglet iTerm2.\n{details}")


def start_linux_terminal(command, cwd, title):
    shell_command = (
        f"cd {shlex.quote(str(cwd))} && "
        f"{shlex.join(command)}; exec bash"
    )
    terminal_commands = [
        ["gnome-terminal", "--title", title, "--", "bash", "-c", shell_command],
        ["konsole", "--new-tab", "-p", f"tabtitle={title}", "-e", "bash", "-c", shell_command],
        ["x-terminal-emulator", "-e", "bash", "-c", shell_command],
    ]

    for terminal_command in terminal_commands:
        if command_exists(terminal_command[0]):
            subprocess.Popen(terminal_command, cwd=cwd)
            return

    fail(
        "Aucun terminal graphique compatible trouvé. "
        f"Lance manuellement « {shlex.join(command)} » "
        f"dans {cwd}."
    )


def start_service(os_name, command, cwd, title):
    service = "backend" if cwd == BACKEND_DIR else "frontend"
    service_command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--service",
        service,
    ]
    if os_name == "windows":
        if os.environ.get("WT_SESSION") and command_exists("wt.exe"):
            start_windows_terminal(service_command, cwd, title)
        else:
            start_windows_console(service_command, cwd, title)
    elif os_name == "mac":
        start_mac_terminal(service_command, cwd, title)
    else:
        start_linux_terminal(service_command, cwd, title)


def start_services(os_name):
    backend_command = (
        BACKEND_COMMAND if os_name == "windows" else BACKEND_COMMAND_UNIX
    )
    services = [
        ("Backend - Spring Boot", backend_command, BACKEND_DIR),
        (
            "Frontend - Vue",
            [npm_executable(os_name), "run", "dev"],
            FRONTEND_DIR,
        ),
    ]

    for title, command, cwd in services:
        print(f"🚀 Démarrage de {title}...")
        print(f"   {subprocess.list2cmdline(command)}")
        try:
            start_service(os_name, command, cwd, title)
        except OSError as error:
            fail(f"Impossible d'ouvrir le terminal pour {title} : {error}")
        print(f"✓ {title} lancé")
        print()


# ============================================================
# Main
# ============================================================

def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Lance ou arrête le projet Vue Training.")
    parser.add_argument(
        "--stop",
        action="store_true",
        help="arrête le frontend, le backend et PostgreSQL",
    )
    parser.add_argument(
        "--service",
        choices=("backend", "frontend"),
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    if args.service:
        raise SystemExit(run_service(args.service))

    print_header()
    should_stop = args.stop or choose_action() == "stop"
    if should_stop:
        if not stop_project():
            raise SystemExit(1)
        print("\n✅ Projet arrêté.")
        return

    os_name = choose_os()

    print()
    print(f"OS sélectionné : {os_name}")
    print()

    check_project_structure()
    check_dependencies(os_name)

    start_docker()
    start_services(os_name)

    print("=" * 60)
    print("✅ PROJET LANCÉ")
    print("=" * 60)
    print()
    print("Frontend : http://localhost:5173")
    print("Backend  : http://localhost:8080")
    print()
    print("Pour tout arrêter proprement, relance « python run.py --stop ».")
    print()


if __name__ == "__main__":
    main()
