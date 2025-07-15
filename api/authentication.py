from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')
        if api_key == getattr(settings, 'WORKER_API_KEY', None):
            return (None, None)
        raise AuthenticationFailed('Invalid API Key')