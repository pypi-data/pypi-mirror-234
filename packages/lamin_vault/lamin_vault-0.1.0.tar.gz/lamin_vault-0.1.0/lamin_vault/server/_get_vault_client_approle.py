import os

import hvac

from lamin_vault.utils.connector import Environment

vault_client_approle = hvac.Client(
    url=Environment().vault_server_url,
    namespace="admin",
)


def get_vault_approle_client():
    if not ("VAULT_ROLE_ID" in os.environ and "VAULT_SECRET_ID" in os.environ):
        raise OSError(
            "App role client can only be retrieve server side when"
            " VAULT_ROLE_ID and VAULT_SECRET_ID are set"
        )
    if not vault_client_approle.is_authenticated():
        vault_client_approle.auth.approle.login(
            role_id=os.environ["VAULT_ROLE_ID"],
            secret_id=os.environ["VAULT_SECRET_ID"],
        )
    return vault_client_approle
