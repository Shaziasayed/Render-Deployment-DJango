from rest_framework.authentication import BaseAuthentication
from .auth_utils import get_or_create_user_from_token

class GoogleTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            user = get_or_create_user_from_token(token)
            if user:
                return (user, None)
        except Exception:
            return None
