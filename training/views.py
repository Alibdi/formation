from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Formation, Participation, PrioriteFormation, DocumentFormation
from .serializers import (
    FormationSerializer, ParticipationSerializer, 
    PrioriteFormationSerializer, DocumentFormationSerializer
)
from .utils import generate_ordre_mission_pdf

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    filterset_fields = ['type']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.role in ['ADMIN', 'OPERATEUR']):
            return Formation.objects.all()
        return Formation.objects.filter(statut=Formation.StatutFormation.PUBLIEE)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            user = self.request.user
            if user.role in ['ADMIN', 'OPERATEUR']:
                return [permissions.IsAuthenticated()]
            return [permissions.IsAdminUser()] # Default fail if not in list
        return [permissions.IsAuthenticated()]

class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    filterset_fields = ['statut', 'agent', 'formation']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'OPERATEUR']:
            return Participation.objects.all()
        elif user.role == 'RESPONSABLE':
            return Participation.objects.filter(agent__service=user.service)
        return Participation.objects.filter(agent=user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        formation_id = data.get('formation')
        
        try:
            formation = Formation.objects.get(id=formation_id)
        except (Formation.DoesNotExist, TypeError):
            return Response({"error": "Formation non trouvée."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check capacity
        if formation.participants.count() >= formation.capacite:
            return Response(
                {"error": "La capacité maximale de cette formation est atteinte."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set the agent
        if request.user.role == 'AGENT':
            data['agent'] = request.user.id
        # OPERATEUR and ADMIN can specify the agent in data
        
        # Prevent double registration
        agent_id = data.get('agent')
        if Participation.objects.filter(agent_id=agent_id, formation=formation).exists():
            return Response(
                {"error": "L'agent est déjà inscrit à cette formation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def export_excel(self, request):
        import openpyxl
        from django.http import HttpResponse
        
        # Only ADMIN or OPERATEUR can export
        if request.user.role not in ['ADMIN', 'OPERATEUR']:
            return Response({"error": "Action non autorisée."}, status=status.HTTP_403_FORBIDDEN)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Participations"
        
        # Headers
        headers = ['ID', 'Agent', 'Matricule', 'Service', 'Formation', 'Type', 'Statut', 'Date Inscription']
        ws.append(headers)
        
        # Data
        participations = self.get_queryset()
        for p in participations:
            ws.append([
                p.id,
                f"{p.agent.first_name} {p.agent.last_name}",
                p.agent.matricule,
                p.agent.service.nom if p.agent.service else '---',
                p.formation.titre,
                p.formation.type,
                p.statut,
                p.date_inscription.strftime('%d/%m/%Y')
            ])
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="participations_formations.xlsx"'
        wb.save(response)
        return response

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def valider(self, request, pk=None):
        participation = self.get_object()
        user = request.user
        
        # Only Admin or Service Manager of the agent can validate
        if user.role == 'ADMIN' or (user.role == 'RESPONSABLE' and user.service == participation.agent.service):
            participation.statut = Participation.Statut.VALIDE
            participation.date_validation = timezone.now()
            participation.save()
            
            # Generate PDF
            try:
                generate_ordre_mission_pdf(participation)
            except Exception as e:
                return Response({"warning": f"Validé mais erreur PDF: {str(e)}", "id": participation.id}, status=status.HTTP_200_OK)
            
            return Response({"status": "Participation validée et ordre de mission généré."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Permissions insuffisantes."}, status=status.HTTP_403_FORBIDDEN)

class DocumentFormationViewSet(viewsets.ModelViewSet):
    queryset = DocumentFormation.objects.all()
    serializer_class = DocumentFormationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return DocumentFormation.objects.all()
        return DocumentFormation.objects.filter(participation__agent=user)

class PrioriteFormationViewSet(viewsets.ModelViewSet):
    queryset = PrioriteFormation.objects.all()
    serializer_class = PrioriteFormationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'OPERATEUR']:
            return PrioriteFormation.objects.all()
        elif user.role == 'RESPONSABLE':
            return PrioriteFormation.objects.filter(service=user.service)
        return PrioriteFormation.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'RESPONSABLE':
            serializer.save(service=user.service)
        else:
            serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            user = self.request.user
            if user.role in ['ADMIN', 'OPERATEUR', 'RESPONSABLE']:
                return [permissions.IsAuthenticated()]
            return [permissions.BasePermission()] # Deny
        return super().get_permissions()
