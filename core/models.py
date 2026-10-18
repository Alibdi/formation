from django.db import models
from django.contrib.auth.models import AbstractUser

class Service(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du service")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code service")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.nom

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrateur'
        OPERATEUR = 'OPERATEUR', 'Chef de Formation'
        RESPONSABLE = 'RESPONSABLE', 'Responsable de Service'
        AGENT = 'AGENT', 'Agent'

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.AGENT,
        verbose_name="Rôle"
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='agents',
        verbose_name="Service"
    )
    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Matricule")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_operateur(self):
        return self.role == self.Role.OPERATEUR

    @property
    def is_responsable(self):
        return self.role == self.Role.RESPONSABLE

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.get_full_name()} ({self.matricule})" if self.matricule else self.username
