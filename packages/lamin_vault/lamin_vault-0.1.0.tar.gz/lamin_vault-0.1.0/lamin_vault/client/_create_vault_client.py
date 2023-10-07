import hvac
import requests  # type: ignore

from lamin_vault.server._create_instance_admin_token_from_jwt import (
    create_instance_admin_token_from_jwt,
)
from lamin_vault.server._create_token_from_jwt import create_token_from_jwt
from lamin_vault.server._get_vault_client_approle import get_vault_approle_client
from lamin_vault.utils.connector import Environment


def create_vault_anonymous_client():
    return hvac.Client(
        url=Environment().vault_server_url,
        namespace="admin",
    )


def create_vault_authenticated_client(access_token, instance_id, server_side=False):
    if server_side:
        vault_client_approle = get_vault_approle_client()
        vault_access_token = create_token_from_jwt(
            vault_client_approle=vault_client_approle,
            access_token=access_token,
            instance_id=instance_id,
        )
    else:
        vault_access_token = requests.post(
            f"{Environment().hub_rest_server_url}/vault/token/from-jwt/{instance_id}",
            headers={"authentication": f"Bearer {access_token}"},
        ).json()
    vault_client = create_vault_anonymous_client()
    vault_client.auth_cubbyhole(vault_access_token)
    return vault_client


def create_vault_admin_client(access_token, instance_id, server_side=False):
    if server_side:
        vault_client_approle = get_vault_approle_client()
        vault_access_token = create_instance_admin_token_from_jwt(
            vault_client_approle=vault_client_approle,
            access_token=access_token,
            instance_id=instance_id,
        )
    else:
        vault_access_token = requests.post(
            f"{Environment().hub_rest_server_url}/vault/token/from-jwt/admin/{instance_id}",
            headers={"authentication": f"Bearer {access_token}"},
        ).json()
    vault_client = create_vault_anonymous_client()
    vault_client.auth_cubbyhole(vault_access_token)
    return vault_client
