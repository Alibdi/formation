from django.contrib import admin
from .models import Formation, Participation, PrioriteFormation, DocumentFormation

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'date_debut', 'date_fin', 'lieu', 'capacite')
    list_filter = ('type', 'date_debut')
    search_fields = ('titre', 'lieu')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('agent', 'formation', 'statut', 'date_inscription', 'date_validation')
    list_filter = ('statut', 'date_inscription')
    search_fields = ('agent__username', 'formation__titre', 'agent__matricule')
    actions = ['valider_participations']

    def valider_participations(self, request, queryset):
        for participation in queryset:
            # We call the validation logic here if needed, 
            # but usually, it's better to do it through the view or a service layer.
            participation.statut = Participation.Statut.VALIDE
            participation.save()
    valider_participations.short_description = "Valider les participations sélectionnées"

@admin.register(PrioriteFormation)
class PrioriteFormationAdmin(admin.ModelAdmin):
    list_display = ('service', 'formation', 'priorite')
    list_filter = ('service',)

@admin.register(DocumentFormation)
class DocumentFormationAdmin(admin.ModelAdmin):
    list_display = ('participation', 'type', 'date_upload')
    list_filter = ('type',)
