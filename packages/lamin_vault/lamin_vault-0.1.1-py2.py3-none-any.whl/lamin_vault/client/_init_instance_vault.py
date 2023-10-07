from lamin_vault.client.postgres._create_or_update_connection_config_db import (
    create_or_update_connection_config_db,
)
from lamin_vault.client.postgres._set_db_role import set_admin_db_role


def init_instance_vault(
    vault_admin_client,
    instance_id,
    admin_account_id,
    db_host,
    db_port,
    db_name,
    vault_db_username,
    vault_db_password,
):
    create_or_update_connection_config_db(
        vault_admin_client=vault_admin_client,
        instance_id=instance_id,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        vault_db_username=vault_db_username,
        vault_db_password=vault_db_password,
    )

    set_admin_db_role(
        vault_admin_client=vault_admin_client,
        instance_id=instance_id,
        account_id=admin_account_id,
    )
