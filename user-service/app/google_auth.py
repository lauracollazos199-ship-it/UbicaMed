from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "575523896419-jl0b1qdq8fblhkka7icqr39er72nmpo7.apps.googleusercontent.com"


def verificar_token_google(token: str):

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        return idinfo

    except ValueError:
        return None