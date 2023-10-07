from hvac.exceptions import InvalidPath

from lamin_vault.client.postgres._delete_db_role import delete_db_role
from lamin_vault.client.postgres._role_and_policy_exist import role_and_policy_exist
from lamin_vault.client.postgres._set_db_role import set_admin_db_role


def test_delete_db_role(instance_context_with_vault):
    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]
    instance_id = instance_context_with_vault["instance_id"]
    admin_account_id = instance_context_with_vault["account_id"]
    role_name = instance_context_with_vault["role_name"]
    policy_name = f"{role_name}-policy"

    # Create a role and policy
    set_admin_db_role(vault_admin_client_test, instance_id, admin_account_id)

    # Verify that the role and policy exist
    assert role_and_policy_exist(
        vault_client=vault_admin_client_test,
        instance_id=instance_id,
        account_id=admin_account_id,
    ), "Admin role and policy should exist in vault."

    # Delete the role and policy
    delete_db_role(vault_admin_client_test, instance_id, admin_account_id)

    # Verify that the role and policy no longer exist
    assert not role_and_policy_exist(
        vault_client=vault_admin_client_test,
        instance_id=instance_id,
        account_id=admin_account_id,
    ), "Admin role and policy should not exist in vault."

    # Verify that the role and policy no longer exist
    try:
        vault_admin_client_test.secrets.database.read_role(name=role_name)
    except InvalidPath:
        pass
    else:
        assert False, "Admin role should not exist in vault."

    try:
        vault_admin_client_test.sys.read_policy(name=policy_name)
    except InvalidPath:
        pass
    else:
        assert False, "Admin policy should not exist in vault."
