# Système de Gestion des Formations des Agents

Une application web complète pour la gestion du cycle de vie des formations, de l'inscription à la génération de l'ordre de mission PDF.

## 🚀 Fonctionnalités

- **Gestion des Formations** : Création, modification et suivi des formations locales et externes.
- **Gestion des Agents & Services** : Organisation par services avec rôles spécifiques (Admin, Responsable, Agent).
- **Workflow d'Inscription** : 
    1. L'agent s'inscrit à une formation (sous réserve de capacité).
    2. Le responsable de service ou l'admin valide l'inscription.
    3. **Génération automatique** de l'Ordre de Mission en PDF via WeasyPrint.
- **Suivi & Documents** : Téléchargement d'attestations, rapports et certificats après la formation.
- **Dashboard Moderne** : Interface fluide construite avec TailwindCSS.

## 🛠️ Installation

### Développement local

1. **Environnement virtuel & Dépendances** :
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Migrations & Données initiales** :
   ```bash
   python manage.py migrate
   python scripts/populate_db.py
   ```

3. **Lancement** :
   ```bash
   python manage.py runserver
   ```

Le lancement local utilise SQLite par défaut. Pour exécuter l'application et PostgreSQL avec Docker, copiez `.env.example` vers `.env`, générez un secret avec `python -c "import secrets; print(secrets.token_urlsafe(64))"`, remplacez aussi le mot de passe PostgreSQL, puis utilisez `DJANGO_DEBUG=true`, `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`, `DJANGO_SECURE_SSL_REDIRECT=false` et `DJANGO_SECURE_HSTS_SECONDS=0` avant `docker compose up --build`.

### Déploiement Coolify

1. Créez une ressource **Docker Compose** reliée au dépôt. Coolify doit utiliser `compose.yaml` à la racine.
2. Configurez le domaine du service `web` sur le port interne `8000`.
3. Ajoutez les variables de `.env.example` dans la configuration d'environnement Coolify. Définissez `DJANGO_SECRET_KEY` avec un secret généré (ne laissez pas la valeur vide); `DJANGO_ALLOWED_HOSTS` attend le nom d'hôte seul et `CSRF_TRUSTED_ORIGINS` une URL complète, par exemple `https://formation.example.com`.
4. Déployez. L'image collecte les fichiers statiques, le conteneur applique les migrations puis démarre Gunicorn. PostgreSQL et les fichiers médias sont conservés dans les volumes `postgres_data` et `media_data`.

La base PostgreSQL créée par Compose est vide : les données du `db.sqlite3` local ne sont pas transférées automatiquement. Sauvegardez également les volumes PostgreSQL et médias dans votre stratégie de sauvegarde.

## 🔐 Accès par défaut (créés par le script de population)

- **Admin** : `admin` / `admin123`
- **Responsable IT** : `resp_it` / `resp123`
- **Agent IT** : `agent1` / `agent123`

## 📂 Structure du Projet

- `core/` : Gestion des utilisateurs (AbstractUser) et des services.
- `training/` : Logique métier des formations, participations et génération PDF.
- `templates/` : Dashboard frontend (TailwindCSS).
- `media/` : Stockage des PDF générés et documents téléchargés.
