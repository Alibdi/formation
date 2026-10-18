from django.db import models
from django.conf import settings
from core.models import Service

class Formation(models.Model):
    class TypeFormation(models.TextChoices):
        LOCALE = 'LOCALE', 'Locale'
        EXTERNE = 'EXTERNE', 'Externe'

    class StatutFormation(models.TextChoices):
        BROUILLON = 'BROUILLON', 'Brouillon'
        PUBLIEE = 'PUBLIEE', 'Publiée'
        ARCHIVEE = 'ARCHIVEE', 'Archivée'

    titre = models.CharField(max_length=255, verbose_name="Titre de la formation")
    type = models.CharField(max_length=10, choices=TypeFormation.choices, verbose_name="Type")
    statut = models.CharField(
        max_length=15, 
        choices=StatutFormation.choices, 
        default=StatutFormation.PUBLIEE,
        verbose_name="Statut"
    )
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(verbose_name="Date de fin")
    lieu = models.CharField(max_length=255, verbose_name="Lieu")
    capacite = models.PositiveIntegerField(verbose_name="Capacité maximale")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def __str__(self):
        return self.titre

class Participation(models.Model):
    class Statut(models.TextChoices):
        INSCRIT = 'INSCRIT', 'Inscrit'
        VALIDE = 'VALIDE', 'Validé'
        REFUSE = 'REFUSE', 'Refusé'
        TERMINE = 'TERMINE', 'Terminé'

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='participations',
        verbose_name="Agent"
    )
    formation = models.ForeignKey(
        Formation, 
        on_delete=models.CASCADE, 
        related_name='participants',
        verbose_name="Formation"
    )
    statut = models.CharField(
        max_length=20, 
        choices=Statut.choices, 
        default=Statut.INSCRIT,
        verbose_name="Statut"
    )
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    ordre_mission = models.FileField(
        upload_to='ordres_mission/', 
        null=True, 
        blank=True,
        verbose_name="Ordre de mission (PDF)"
    )

    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        unique_together = ('agent', 'formation')

    def __str__(self):
        return f"{self.agent} - {self.formation}"

class PrioriteFormation(models.Model):
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='priorites',
        verbose_name="Service"
    )
    formation = models.ForeignKey(
        Formation, 
        on_delete=models.CASCADE, 
        related_name='priorites_service',
        verbose_name="Formation"
    )
    priorite = models.PositiveIntegerField(default=1, verbose_name="Niveau de priorité")

    class Meta:
        verbose_name = "Priorité de Formation"
        verbose_name_plural = "Priorités de Formations"
        unique_together = ('service', 'formation')

class DocumentFormation(models.Model):
    class TypeDoc(models.TextChoices):
        ATTESTATION = 'ATTESTATION', 'Attestation'
        RAPPORT = 'RAPPORT', 'Rapport'
        CERTIFICAT = 'CERTIFICAT', 'Certificat'

    participation = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE, 
        related_name='documents',
        verbose_name="Participation"
    )
    fichier = models.FileField(upload_to='documents_formation/', verbose_name="Fichier")
    type = models.CharField(max_length=20, choices=TypeDoc.choices, verbose_name="Type de document")
    date_upload = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")

    class Meta:
        verbose_name = "Document de Formation"
        verbose_name_plural = "Documents de Formations"
