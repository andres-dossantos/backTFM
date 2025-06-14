"""
URL configuration for financeManagerApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from auth.views import EmailTokenObtainPairView, UserRegistrationView
from users.urls import urlpatterns as user_urls
from forms.urls import forms_url_patterns
from predictions.urls import predictions_url_patterns

api_urlpatterns = [
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('', include(user_urls), name='user'),
    path('', include(forms_url_patterns), name='form'),
    path('', include(predictions_url_patterns), name='prediction'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="docs"
    ),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((api_urlpatterns, 'api'), namespace='api')),
]
