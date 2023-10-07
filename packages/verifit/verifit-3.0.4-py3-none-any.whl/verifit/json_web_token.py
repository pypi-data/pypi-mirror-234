import datetime
import jwt


def get_token_expiration_date(decoded_token):
    token_expiry_ms = decoded_token.get('exp', None)
    assert token_expiry_ms is not None
    token_expiry_date = datetime.datetime.fromtimestamp(token_expiry_ms)
    return token_expiry_date


def decode_token(access_token):
    decoded_token = jwt.decode(access_token, algorithms=["RS256", "HS256"], options={"verify_signature": False})
    return decoded_token
