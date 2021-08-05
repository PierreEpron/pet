from django.urls import include, path
from rest_framework import routers
from authentification import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import DocumentViewSet, ProjectViewSet, upload, random_document, apply_queue

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'api/documents', DocumentViewSet)
router.register(r'api/projects', ProjectViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/upload/', upload, name='upload_csv'),
    path('api/random/', random_document, name='random_document'),
    path('api/apply-queue/', apply_queue, name='apply_queue'),
]