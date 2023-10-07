from lamin_vault.client.postgres._connection_config_db_exists import (
    connection_config_db_exists,
)
from lamin_vault.client.postgres._role_and_policy_exist import role_and_policy_exist


def test_init_instance_vault(instance_context_with_vault):
    instance_id = instance_context_with_vault["instance_id"]
    admin_account_id = instance_context_with_vault["account_id"]

    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]

    # Verify connection configuration exists
    assert connection_config_db_exists(
        vault_client=vault_admin_client_test, instance_id=instance_id
    ), "Connection configuration should exist in vault."

    # Verify connection admin role and policy exist
    assert role_and_policy_exist(
        vault_client=vault_admin_client_test,
        instance_id=instance_id,
        account_id=admin_account_id,
    ), "Admin role and policy should exist in vault."
