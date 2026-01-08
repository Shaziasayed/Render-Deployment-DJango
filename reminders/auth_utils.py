from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User

GOOGLE_CLIENT_ID = "431581942890-8jh3ce0rdahcuncrggkoo25svpdid1us.apps.googleusercontent.com"

def get_or_create_user_from_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo["email"]
        name = idinfo.get("name", email)

        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email, "first_name": name}
        )

        return user

    except Exception:
        return None
