from ninja.errors import HttpError
from ninja.security import HttpBearer
from rest_framework_api_key.models import APIKey


class HasAPIKey(HttpBearer):
    def authenticate(self, request, token):
        try:
            key = APIKey.objects.get_from_key(token)
            if key is not None and key.is_valid:
                return key  # ou key.name se quiser identificar
        except Exception:
            pass
        raise HttpError(403, "Unauthorized: Invalid API Key")
