import os
import django
import sys
from datetime import datetime, timedelta
from django.utils import timezone

# Setup django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_system.settings')
django.setup()

from core.models import Service, User
from training.models import Formation, Participation

def populate():
    print("Populating database...")
    
    # 1. Create Services
    it_service, _ = Service.objects.get_or_create(nom="Informatique", code="IT")
    hr_service, _ = Service.objects.get_or_create(nom="Ressources Humaines", code="RH")
    sales_service, _ = Service.objects.get_or_create(nom="Ventes", code="SALES")
    
    # 2. Create Users
    admin, _ = User.objects.get_or_create(
        username="admin", 
        defaults={
            "role": User.Role.ADMIN,
            "is_staff": True,
            "is_superuser": True,
            "first_name": "Admin",
            "last_name": "System"
        }
    )
    admin.set_password("admin123")
    admin.save()
    
    resp_it, _ = User.objects.get_or_create(
        username="resp_it",
        defaults={
            "role": User.Role.RESPONSABLE,
            "service": it_service,
            "first_name": "Jean",
            "last_name": "Responsable"
        }
    )
    resp_it.set_password("resp123")
    resp_it.save()
    
    agent1, _ = User.objects.get_or_create(
        username="agent1",
        defaults={
            "role": User.Role.AGENT,
            "service": it_service,
            "matricule": "AG001",
            "first_name": "Paul",
            "last_name": "Agent"
        }
    )
    agent1.set_password("agent123")
    agent1.save()
    
    # 3. Create Formations
    f1, _ = Formation.objects.get_or_create(
        titre="Python pour Data Science",
        defaults={
            "type": Formation.TypeFormation.LOCALE,
            "date_debut": timezone.now() + timedelta(days=10),
            "date_fin": timezone.now() + timedelta(days=12),
            "lieu": "Salle 101",
            "capacite": 10,
            "description": "Apprendre les bases de Python pour la data science."
        }
    )
    
    f2, _ = Formation.objects.get_or_create(
        titre="Communication Non-Violente",
        defaults={
            "type": Formation.TypeFormation.EXTERNE,
            "date_debut": timezone.now() + timedelta(days=20),
            "date_fin": timezone.now() + timedelta(days=21),
            "lieu": "Centre de Conférences",
            "capacite": 25,
            "description": "Améliorer la communication interpersonnelle."
        }
    )
    
    # 4. Create Participations
    p1, _ = Participation.objects.get_or_create(
        agent=agent1,
        formation=f1,
        defaults={"statut": Participation.Statut.INSCRIT}
    )
    
    print("Database populated successfully!")

if __name__ == "__main__":
    populate()
