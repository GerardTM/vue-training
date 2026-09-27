# Vue Training

Application web de formation composée d'un frontend Vue 3 et d'une API Spring Boot. Le backend gère les comptes utilisateur et l'authentification par JWT ; l'interface frontend contient les vues d'accueil, référentiel, import, produits, logs et profil.

## Sommaire

- [Technologies](#technologies)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Configuration](#configuration)
- [Lancer le projet](#lancer-le-projet)
- [API disponible](#api-disponible)
- [Tests et compilation](#tests-et-compilation)
- [Arrêter et réinitialiser](#arrêter-et-réinitialiser)
- [Sécurité](#sécurité)
- [Dépannage](#dépannage)

## Technologies

- Frontend : Vue 3, TypeScript, Vite, Pinia, Vue Router, Tailwind CSS
- Backend : Java 21, Spring Boot, Spring Security, Spring Data JPA, Flyway
- Base de données : PostgreSQL 17
- Environnement local : Docker Compose, Gradle Wrapper, npm

## Architecture

```text
Navigateur (Vue / Vite : http://localhost:5173)
        │ HTTP / JSON, JWT
        ▼
API Spring Boot (http://localhost:8080/api)
        │ JPA / JDBC
        ▼
PostgreSQL (localhost:5432)
```

Le backend suit une séparation par couches : contrôleurs, services, repositories et entités. Flyway applique les migrations SQL au démarrage de Spring Boot.

## Prérequis

- Java 21
- Node.js `^22.18.0` ou `>=24.12.0` et npm
- Docker Desktop avec Docker Compose
- Git

Vérifier les outils :

```bash
java -version
node --version
npm --version
docker compose version
```

## Configuration

### Backend et PostgreSQL

Depuis la racine du dépôt, crée le fichier local s'il n'existe pas déjà :

```bash
cp -n backend/.env.example backend/.env
```

Dans `backend/.env`, définis les identifiants PostgreSQL locaux et remplace `JWT_SECRET` par une clé aléatoire d'au moins 32 octets. Pour en générer une :

```bash
openssl rand -hex 32
```

Le fichier `backend/.env` est ignoré par Git. Il fournit les paramètres à Docker Compose et à Spring Boot. Les principales variables sont :

| Variable            | Utilisation                                         |
| ------------------- | --------------------------------------------------- |
| `POSTGRES_DB`       | Nom de la base PostgreSQL                           |
| `POSTGRES_USER`     | Utilisateur PostgreSQL                              |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL                             |
| `DB_HOST`           | Hôte utilisé par le backend, `localhost` par défaut |
| `DB_PORT`           | Port PostgreSQL, `5432` par défaut                  |
| `JWT_SECRET`        | Clé de signature des jetons JWT                     |

### Frontend

Le frontend utilise par défaut `http://localhost:8080/api`. Pour changer cette adresse, crée `frontend/.env.local` à partir de l'exemple :

```bash
cp -n frontend/.env.example frontend/.env.local
```

Puis ajuste `VITE_API_BASE_URL`. Les variables `VITE_*` sont intégrées au code livré au navigateur : n'y place aucun secret.

## Lancer le projet

Les commandes suivantes partent de la racine du dépôt, sauf indication contraire.

1. Démarrer PostgreSQL :

```bash
docker compose -f backend/docker-compose.yml up -d
```

2. Démarrer l'API dans un terminal :

```bash
cd backend
./gradlew bootRun
```

Sous Windows, utiliser `gradlew.bat bootRun`.

3. Installer les dépendances et démarrer le frontend dans un autre terminal :

```bash
cd frontend
npm ci
npm run dev
```

L'application frontend est disponible à [http://localhost:5173](http://localhost:5173). L'API est disponible à [http://localhost:8080](http://localhost:8080).

## API disponible

Les routes sont préfixées par `/api`. Les corps et réponses utilisent JSON.

| Méthode | Route             | Accès      | Description                                                         |
| ------- | ----------------- | ---------- | ------------------------------------------------------------------- |
| `POST`  | `/api/auth/login` | Public     | Connexion ; renvoie un JWT et le profil utilisateur                 |
| `POST`  | `/api/users`      | Public     | Création d'un compte (`email`, `password`, `firstName`, `lastName`) |
| `GET`   | `/api/users`      | JWT requis | Liste des utilisateurs                                              |
| `GET`   | `/api/users/me`   | JWT requis | Profil associé au JWT                                               |

Pour les routes protégées, envoyer le jeton ainsi :

```http
Authorization: Bearer <token>
```

Les autres écrans du frontend ne correspondent pas nécessairement à des endpoints backend : à ce stade, l'API implémente les routes d'authentification et de gestion des utilisateurs listées ci-dessus.

## Tests et compilation

Backend, depuis `backend/` :

```bash
./gradlew test
./gradlew build
```

Le build Gradle exécute également Spotless pour formater le code Java.

Frontend, depuis `frontend/` :

```bash
npm run build
```

Cette commande vérifie les types TypeScript/Vue et génère les fichiers de production dans `frontend/dist/`.

## Arrêter et réinitialiser

Arrêter le backend avec `Ctrl+C`, puis arrêter PostgreSQL depuis la racine :

```bash
docker compose -f backend/docker-compose.yml down
```

Les données PostgreSQL sont conservées dans un volume Docker. Pour supprimer aussi ce volume et toutes les données de la base :

```bash
docker compose -f backend/docker-compose.yml down -v
```

## Sécurité

- Ne versionne jamais `backend/.env` ni d'autres fichiers contenant des secrets.
- Génère une clé `JWT_SECRET` aléatoire et distincte pour chaque environnement ; ne réutilise pas la valeur d'exemple en production.
- Les mots de passe utilisateur sont encodés avec BCrypt.
- Les variables `VITE_*` sont publiques une fois compilées.
- La configuration CORS actuelle autorise le frontend local à `http://localhost:5173`. Adapte cette origine avant un déploiement.

## Dépannage

- **Docker ne répond pas** : démarre Docker Desktop, puis vérifie `docker info`.
- **Le port 5432 est occupé** : arrête l'autre service PostgreSQL ou change le mapping dans `backend/docker-compose.yml` et ajuste `DB_PORT` dans `backend/.env`.
- **L'API ne démarre pas** : vérifie la présence de `backend/.env`, les valeurs de connexion et l'état du conteneur avec `docker compose -f backend/docker-compose.yml logs postgres`.
- **Le frontend ne joint pas l'API** : vérifie que le backend écoute sur le port 8080 et que `VITE_API_BASE_URL` pointe vers `/api`. L'origine CORS du backend est actuellement limitée à `http://localhost:5173`.
