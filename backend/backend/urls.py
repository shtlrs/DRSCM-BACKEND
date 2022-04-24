from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("token/", TokenObtainPairView.as_view(), name=TokenObtainPairView.__name__),
    path("token/refresh/", TokenRefreshView.as_view(), name=TokenRefreshView.__name__),
    path(
        "token/blacklist/",
        TokenBlacklistView.as_view(),
        name=TokenBlacklistView.__name__,
    ),
    path("token/verify/", TokenVerifyView.as_view(), name=TokenVerifyView.__name__),
    path("", include("drscm.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
