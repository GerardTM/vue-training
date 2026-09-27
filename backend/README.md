# Vue Training - Backend

Backend de l'application Vue Training développé avec **Spring Boot**.

## 🛠️ Technologies

- Java 21
- Spring Boot
- Gradle
- PostgreSQL
- Docker / Docker Compose
- Spring Data JPA
- Flyway

---

## 📋 Prérequis

Avant de lancer le projet, il faut avoir installé :

- Java 21
- Docker Desktop
- Git

Vérifier Java :

```bash
java -version
```

Vérifier Docker :

```bash
docker --version
docker compose version
```

Vérifier que Docker fonctionne :

```bash
docker info
```

---

## 📁 Structure du projet

```text
backend/
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   │
│   └── test/
│
├── docker-compose.yml
├── build.gradle
├── settings.gradle
├── gradlew
├── gradlew.bat
└── README.md
```

---

## 🐘 PostgreSQL

Le projet utilise PostgreSQL dans un conteneur Docker.

### Configuration

| Paramètre | Valeur                                  |
| --------- | --------------------------------------- |
| Host      | `localhost`                             |
| Port      | `5432`                                  |
| Database  | `POSTGRES_DB` dans `backend/.env`       |
| Username  | `POSTGRES_USER` dans `backend/.env`     |
| Password  | `POSTGRES_PASSWORD` dans `backend/.env` |

---

## 🚀 Lancer le projet

### 1. Démarrer Docker Desktop

Docker Desktop doit être démarré avant de lancer PostgreSQL.

Vérifier que Docker fonctionne :

```bash
docker info
```

---

### 2. Configurer l'environnement

Créer `backend/.env` à partir de l'exemple, puis définir des valeurs locales pour PostgreSQL et `JWT_SECRET` :

```bash
cp backend/.env.example backend/.env
```

Ne pas utiliser ces paramètres locaux en production. `JWT_SECRET` doit être une valeur aléatoire d'au moins 32 octets.

### 3. Démarrer PostgreSQL

Depuis la racine du projet :

```bash
docker compose -f backend/docker-compose.yml up -d
```

Vérifier que le conteneur est bien lancé :

```bash
docker ps
```

---

### 4. Lancer Spring Boot

Depuis le dossier `backend` :

```bash
cd backend
./gradlew bootRun
```

Le backend est alors disponible sur :

```text
http://localhost:8080
```

---

## 🛑 Arrêter le projet

### Arrêter Spring Boot

Dans le terminal où Spring Boot est lancé :

```text
Ctrl + C
```

### Arrêter PostgreSQL

```bash
docker compose down
```

---

## 🔄 Redémarrer le projet

Pour un démarrage classique :

```bash
docker compose up -d
./gradlew bootRun
```

---

## 🗄️ Base de données

La connexion PostgreSQL est configurée dans `backend/.env` et chargée par :

```text
src/main/resources/application.properties
```

Configuration actuelle :

```properties
spring.application.name=vue-training
spring.datasource.url=jdbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5432}/${POSTGRES_DB:office}
spring.datasource.username=${POSTGRES_USER}
spring.datasource.password=${POSTGRES_PASSWORD}
spring.jpa.hibernate.ddl-auto=none
```

---

## 🦋 Flyway

Les migrations de base de données sont gérées avec **Flyway**.

Les fichiers de migration doivent être placés dans :

```text
src/main/resources/db/migration/
```

Exemple :

```text
src/main/resources/db/migration/
└── V1__create_users.sql
```

Les migrations seront exécutées automatiquement par Spring Boot lors du démarrage.

---

## ☕ Java

Le projet utilise **Java 21**.

La version Java utilisée par Gradle est définie dans `build.gradle` :

```groovy
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

Vérifier les versions Java détectées par Gradle :

```bash
./gradlew -q javaToolchains
```

---

## 🔨 Commandes Gradle

### Compiler le projet

```bash
./gradlew build
```

### Lancer les tests

```bash
./gradlew test
```

### Nettoyer le projet

```bash
./gradlew clean
```

### Nettoyer et compiler

```bash
./gradlew clean build
```

### Lancer Spring Boot

```bash
./gradlew bootRun
```

---

## 🐳 Commandes Docker

### Démarrer PostgreSQL

```bash
docker compose up -d
```

### Arrêter PostgreSQL

```bash
docker compose down
```

### Voir les conteneurs actifs

```bash
docker ps
```

### Voir les logs PostgreSQL

```bash
docker compose logs postgres
```

### Voir les logs en temps réel

```bash
docker compose logs -f postgres
```

---

## 🧹 Réinitialiser la base de données

⚠️ Cette commande supprime le conteneur ainsi que le volume PostgreSQL et donc **toutes les données de la base**.

```bash
docker compose down -v
```

Puis recréer PostgreSQL :

```bash
docker compose up -d
```

---

## 🌐 Architecture

```text
┌─────────────────────┐
│       Vue 3         │
│   localhost:5173    │
└──────────┬──────────┘
           │
           │ HTTP / JSON
           ▼
┌─────────────────────┐
│     Spring Boot     │
│   localhost:8080    │
│                     │
│  Controller         │
│      ↓              │
│  Service            │
│      ↓              │
│  Repository         │
│      ↓              │
│  JPA                │
└──────────┬──────────┘
           │
           │ JDBC
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│   localhost:5432    │
│                     │
│      office         │
└─────────────────────┘
```

---

## 🔧 Configuration du frontend

Le frontend Vue 3 communiquera avec le backend via l'API REST :

```text
Frontend
http://localhost:5173

        ↓ HTTP

Backend
http://localhost:8080/api
```

Les endpoints de l'API seront regroupés sous :

```text
/api
```

Exemple :

```text
GET    /api/users
GET    /api/users/{id}
POST   /api/users
PUT    /api/users/{id}
DELETE /api/users/{id}
```

---

## ⚠️ Problèmes fréquents

### Docker daemon inaccessible

Si vous obtenez :

```text
Cannot connect to the Docker daemon
```

vérifiez que **Docker Desktop est démarré**.

Puis :

```bash
docker info
```

---

### PostgreSQL ne démarre pas

Afficher les logs :

```bash
docker compose logs postgres
```

Vérifier si le port `5432` est déjà utilisé :

```bash
lsof -i :5432
```

---

### Spring Boot ne démarre pas

Vérifier que PostgreSQL fonctionne :

```bash
docker ps
```

Puis vérifier :

```text
src/main/resources/application.properties
```

Les paramètres doivent correspondre à ceux du `docker-compose.yml`.

---

### Le port 8080 est déjà utilisé

Vérifier :

```bash
lsof -i :8080
```

Pour changer le port de Spring Boot :

```properties
server.port=8081
```

Le backend sera alors accessible sur :

```text
http://localhost:8081
```

---

## 👨‍💻 Workflow de développement

Pour commencer à travailler sur le projet :

### 1. Démarrer Docker Desktop

### 2. Démarrer PostgreSQL

```bash
docker compose up -d
```

### 3. Vérifier PostgreSQL

```bash
docker ps
```

### 4. Lancer Spring Boot

```bash
./gradlew bootRun
```

### 5. Développer

Le backend est disponible sur :

```text
http://localhost:8080
```

Et le frontend Vue 3 sur :

```text
http://localhost:5173
```

---

## 📌 À venir

- [ ] Configuration complète de Flyway
- [ ] Création des premières entités
- [ ] Création des repositories
- [ ] Création des services
- [ ] Création des controllers REST
- [ ] Gestion globale des erreurs
- [ ] Configuration CORS
- [ ] Authentification
- [ ] Connexion avec le frontend Vue 3
