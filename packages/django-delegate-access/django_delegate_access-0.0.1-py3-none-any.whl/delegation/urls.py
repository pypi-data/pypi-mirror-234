from rest_framework.routers import DefaultRouter
from .views import DelegationViewSet

router = DefaultRouter()
router.register(r'delegations', DelegationViewSet)

urlpatterns = router.urls
