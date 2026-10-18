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

## 🔐 Accès par défaut (créés par le script de population)

- **Admin** : `admin` / `admin123`
- **Responsable IT** : `resp_it` / `resp123`
- **Agent IT** : `agent1` / `agent123`

## 📂 Structure du Projet

- `core/` : Gestion des utilisateurs (AbstractUser) et des services.
- `training/` : Logique métier des formations, participations et génération PDF.
- `templates/` : Dashboard frontend (TailwindCSS).
- `media/` : Stockage des PDF générés et documents téléchargés.
