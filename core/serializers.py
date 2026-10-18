from rest_framework import serializers
from .models import Service, User

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'nom', 'code']

class UserSerializer(serializers.ModelSerializer):
    service_details = ServiceSerializer(source='service', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'role', 'service', 'service_details', 'matricule', 'telephone',
            'is_admin', 'is_operateur', 'is_responsable'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
