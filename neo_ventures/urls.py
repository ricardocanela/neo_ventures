from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from innovation.views import CompanyViewSet, DemandViewSet, SolutionViewSet
from innovation.views import RegisterUserAPIView, UserDetailAPI
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Innovation API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@inovation.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()
router.register('companies', CompanyViewSet, basename='companies')
router.register('demands', DemandViewSet, basename='demands')
router.register('solutions', SolutionViewSet, basename='solutions')

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('accounts/login/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('get-details',UserDetailAPI.as_view()),
    path('register',RegisterUserAPIView.as_view()),
]

urlpatterns += router.urls
