from rest_framework.routers import DefaultRouter
from .views import SavedProductViewSet

router = DefaultRouter()
router.register(r'saved-products', SavedProductViewSet, basename='savedproduct')

urlpatterns = router.urls