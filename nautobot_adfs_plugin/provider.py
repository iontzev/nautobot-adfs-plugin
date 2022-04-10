from django.urls import reverse
from django.shortcuts import redirect
from django_auth_adfs.views import OAuth2LoginView
from django_auth_adfs.config import ProviderConfig


class NautobotProviderConfig(ProviderConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def redirect_uri(self, request):
        self.load_config()
        return request.build_absolute_uri(reverse("plugins:nautobot_adfs_plugin:callback"))

provider_config = NautobotProviderConfig()

class NautobotOAuth2LoginView(OAuth2LoginView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def get(self, request):
        return redirect(provider_config.build_authorization_endpoint(request))
