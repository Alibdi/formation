from rest_framework import serializers
from .models import Formation, Participation, PrioriteFormation, DocumentFormation
from core.serializers import UserSerializer

class FormationSerializer(serializers.ModelSerializer):
    participant_count = serializers.IntegerField(source='participants.count', read_only=True)
    is_full = serializers.SerializerMethodField()
    priorite_pour_mon_service = serializers.SerializerMethodField()

    class Meta:
        model = Formation
        fields = ['id', 'titre', 'type', 'statut', 'date_debut', 'date_fin', 'lieu', 'capacite', 'description', 'participant_count', 'is_full', 'priorite_pour_mon_service']

    def get_is_full(self, obj):
        return obj.participants.count() >= obj.capacite

    def get_priorite_pour_mon_service(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated or not user.service:
            return None
        priorite = obj.priorites_service.filter(service=user.service).first()
        return priorite.priorite if priorite else None

class ParticipationSerializer(serializers.ModelSerializer):
    agent_details = UserSerializer(source='agent', read_only=True)
    formation_details = FormationSerializer(source='formation', read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'
        read_only_fields = ['date_inscription', 'date_validation', 'ordre_mission']

class PrioriteFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioriteFormation
        fields = '__all__'

class DocumentFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFormation
        fields = '__all__'
