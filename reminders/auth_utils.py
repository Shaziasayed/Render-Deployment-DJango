from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

GOOGLE_CLIENT_ID = "431581942890-8jh3ce0rdahcuncrggkoo25svpdid1us.apps.googleusercontent.com"


def get_or_create_user_from_token(token):
    try:
        # Verify Google token
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        name = idinfo.get("name", email)

        if not email:
            return None

        # Get or create user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "first_name": name,
            }
        )

        return user

    except Exception as e:
        print("Google auth error:", e)
        return None


def generate_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
