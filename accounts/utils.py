from django.conf import settings
import uuid
import jwt
import datetime
import pytz


class JWTToken:
    jti = str(uuid.uuid4())

    def generate_access_token(self, user):
        access_token_payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            + settings.ACCESS_EXPIRE_TIME,
            "iat": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran")),
            "jti": self.jti,
        }

        access_token = jwt.encode(
            access_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        return access_token

    def generate_refresh_token(self, user):
        refresh_token_payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            + settings.REFRESH_EXPIRE_TIME,
            "iat": datetime.datetime.now(tz=pytz.timezone("Asia/Tehran")),
            "jti": self.jti,
        }

        refresh_token = jwt.encode(
            refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        return refresh_token
