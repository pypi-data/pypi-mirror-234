from datetime import datetime

from requests.auth import AuthBase

from .cache import cache_set, cache_get
from .config import get_store_reader, get_store_writer
from .date_tools import date_subtract_in_minutes
from .json_web_token import decode_token, get_token_expiration_date

get_env = get_store_reader()
set_env = get_store_writer()

ACCESS_TOKEN = 'accessToken'
EXPIRY_DATE = 'expiryDate'
LOGIN_DATA = 'loginData'


def get_expiry_date(login_data):
    return datetime.fromisoformat(login_data.get(EXPIRY_DATE))


def login(driver=None, username=None, password=None):
    access_token = driver(username=username, password=password)
    decoded_token = decode_token(access_token)
    token_expiry_date = get_token_expiration_date(decoded_token)
    login_data = {
        ACCESS_TOKEN: access_token,
        EXPIRY_DATE: token_expiry_date.isoformat()
    }
    cache_set(username)(login_data)
    set_env(LOGIN_DATA)(login_data)
    return login_data


def get_login_values_from_cache(username):
    user_cached_data = cache_get(username)
    if user_cached_data is None:
        print(f"Cache miss key <{username}>, no cached data")
        return None
    token_expiry_iso_string = user_cached_data.get('expiryDate', None)
    if token_expiry_iso_string is None:
        print(f"Cache miss key <{username}>, no expiration info")
        return None
    token_expiry_date = datetime.fromisoformat(token_expiry_iso_string)
    minutes = date_subtract_in_minutes(from_date=token_expiry_date, date_to_subtract=datetime.now())
    if minutes < 10:
        print(f"Cache miss key <{username}>, almost expired")
        return None
    print(f"Cache hit key <{username}>")
    login_data = {
        ACCESS_TOKEN: user_cached_data.get(ACCESS_TOKEN),
        EXPIRY_DATE: token_expiry_date
    }
    return login_data


def login_from_cache(driver=None, username=None, password=None):
    login_data = get_login_values_from_cache(username)
    if login_data is None:
        login_data = login(driver=driver, username=username, password=password)
    print(f"Caching login data <{login_data}>")
    set_env(LOGIN_DATA)(login_data)
    return login_data


def get_bearer_authorization_header_value():
    login_data = get_env(LOGIN_DATA)
    print(f"Using cached login data <{login_data}>")
    return f"Bearer {login_data.get(ACCESS_TOKEN)}"


def get_bearer_auth_base():
    class BearerAuth(AuthBase):
        def __init__(self, token):
            self.token = token

        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            return r

    login_data = get_env(LOGIN_DATA)
    return BearerAuth(login_data.get(ACCESS_TOKEN))
