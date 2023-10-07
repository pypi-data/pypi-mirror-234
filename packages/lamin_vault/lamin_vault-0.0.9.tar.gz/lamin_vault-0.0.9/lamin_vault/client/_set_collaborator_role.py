from laminhub_rest.routers.utils import extract_access_token

from lamin_vault.client._create_vault_client import create_vault_admin_client
from lamin_vault.client.postgres._create_or_update_role_and_policy_db import (
    create_or_update_role_and_policy_db,
)
from lamin_vault.client.postgres._set_db_role import (
    set_admin_db_role,
    set_read_db_role,
    set_write_db_role,
)


def set_collaborator_role(
    instance_id: str,
    account_id: str,
    role_name: str,
    authentication: str,
    role_creation_statements: list[str] = None,
):
    vault_admin_client = create_vault_admin_client(
        access_token=extract_access_token(authentication),
        instance_id=instance_id,
    )

    if role_creation_statements is not None:
        create_or_update_role_and_policy_db(
            vault_admin_client, instance_id, account_id, role_creation_statements
        )
    else:
        if role_name == "admin":
            set_admin_db_role(vault_admin_client, instance_id, account_id)
        elif role_name == "write":
            set_write_db_role(vault_admin_client, instance_id, account_id)
        elif role_name == "read":
            set_read_db_role(vault_admin_client, instance_id, account_id)
