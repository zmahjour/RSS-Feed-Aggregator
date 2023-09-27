from django.conf import settings
import uuid
import jwt
import datetime


class JWTToken:
    jti = str(uuid.uuid4())

    def generate_access_token(self, user):
        access_token_payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(),
            "jti": self.jti,
        }

        access_token = jwt.encode(
            access_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        return access_token

