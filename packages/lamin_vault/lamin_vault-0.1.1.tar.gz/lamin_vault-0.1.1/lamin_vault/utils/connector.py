# see the overlap with connector.py in laminhub-rest
import os
from typing import Optional
from urllib.request import urlretrieve

from gotrue.errors import AuthUnknownError
from postgrest import APIError as PostgrestAPIError
from pydantic import BaseSettings
from supabase import create_client
from supabase.lib.client_options import ClientOptions


class Connector(BaseSettings):
    url: str
    key: str


def load_fallback_connector() -> Connector:
    url = "https://lamin-site-assets.s3.amazonaws.com/connector.env"
    connector_file, _ = urlretrieve(url)
    connector = Connector(_env_file=connector_file)
    return connector


PROD_URL = "https://hub.lamin.ai"
PROD_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxhZXNhdW1tZHlkbGxwcGdmY2h1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY4NDA1NTEsImV4cCI6MTk3MjQxNjU1MX0.WUeCRiun0ExUxKIv5-CtjF6878H8u26t0JmCWx3_2-c"  # noqa
PROD_HUB_REST_SERVER_URL = (
    "https://laminhub-rest-cloud-run-prod-xv4y7p4gqa-uc.a.run.app"
)

STAGING_URL = "https://amvrvdwndlqdzgedrqdv.supabase.co"
STAGING_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFtdnJ2ZHduZGxxZHpnZWRycWR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzcxNTcxMzMsImV4cCI6MTk5MjczMzEzM30.Gelt3dQEi8tT4j-JA36RbaZuUvxRnczvRr3iyRtzjY0"  # noqa
STAGING_HUB_REST_SERVER_URL = (
    "https://laminhub-rest-cloud-run-staging-xv4y7p4gqa-uc.a.run.app"
)

VAULT_SERVER_URL = (
    "https://vault-cluster-prod-public-vault-775dc7d2.d8b6f751.z1.hashicorp.cloud:8200"
)


class Environment:
    def __init__(self, fallback: bool = False):
        lamin_env = os.getenv("LAMIN_ENV")
        if lamin_env is None:
            lamin_env = "prod"
        # set public key
        if lamin_env == "prod":
            if not fallback:
                url = PROD_URL
                key = PROD_KEY
            else:
                connector = load_fallback_connector()
                url = connector.url
                key = connector.key
            hub_rest_server_url = PROD_HUB_REST_SERVER_URL
            vault_server_url = VAULT_SERVER_URL
        elif lamin_env == "staging":
            url = STAGING_URL
            key = STAGING_KEY
            hub_rest_server_url = STAGING_HUB_REST_SERVER_URL
            vault_server_url = VAULT_SERVER_URL
        else:
            url = os.environ["SUPABASE_API_URL"]
            key = os.environ["SUPABASE_ANON_KEY"]
            hub_rest_server_url = os.environ.get("LAMIN_HUB_REST_SERVER_URL", None)  # type: ignore
            vault_server_url = os.environ["VAULT_SERVER_URL"]
        self.lamin_env: str = lamin_env
        self.supabase_api_url: str = url
        self.supabase_anon_key: str = key
        self.hub_rest_server_url: str = hub_rest_server_url
        self.vault_server_url: str = vault_server_url


def connect_hub(client_options: ClientOptions = ClientOptions()):
    env = Environment()

    return create_client(env.supabase_api_url, env.supabase_anon_key, client_options)


def connect_hub_with_auth(
    *,
    email: Optional[str] = None,
    password: Optional[str] = None,
    access_token: Optional[str] = None,
):
    hub = connect_hub()
    if access_token is None:
        if email is None or password is None:
            from lamindb_setup import settings

            email = settings.user.email
            password = settings.user.password
        access_token = get_access_token(email=email, password=password)
    hub.postgrest.auth(access_token)
    return hub


# def connect_hub_with_service_role():
#    env = Environment()
#    return create_client(env.supabase_api_url, os.environ["SUPABASE_SERVICE_ROLE_KEY"])


def get_access_token(email: Optional[str] = None, password: Optional[str] = None):
    hub = connect_hub()
    try:
        auth_response = hub.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
        return auth_response.session.access_token
    finally:
        hub.auth.sign_out()


def call_with_fallback_auth(
    callable,
    **kwargs,
):
    for renew_token, fallback_env in [(False, False), (True, False), (False, True)]:
        try:
            client = connect_hub_with_auth(
                renew_token=renew_token, fallback_env=fallback_env
            )
            result = callable(**kwargs, client=client)
            break
        except (PostgrestAPIError, AuthUnknownError) as e:
            if fallback_env:
                raise e
        finally:
            client.auth.sign_out()
    return result


def call_with_fallback(
    callable,
    **kwargs,
):
    for fallback_env in [False, True]:
        try:
            client = connect_hub(fallback_env=fallback_env)
            result = callable(**kwargs, client=client)
            break
        except AuthUnknownError as e:
            if fallback_env:
                raise e
        finally:
            # in case there was sign in
            client.auth.sign_out()
    return result
