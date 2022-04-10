from django.urls import path
from . import views
from . import provider

app_name = 'django_auth_adfs'


urlpatterns = [
    path('callback/', views.OAuth2Callback.as_view(), name='callback'),
    path('login/', provider.NautobotOAuth2LoginView.as_view(), name='login'),
]

