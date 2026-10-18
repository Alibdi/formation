from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormationViewSet, ParticipationViewSet, DocumentFormationViewSet, PrioriteFormationViewSet

router = DefaultRouter()
router.register(r'formations', FormationViewSet)
router.register(r'participations', ParticipationViewSet)
router.register(r'documents', DocumentFormationViewSet)
router.register(r'priorites', PrioriteFormationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
