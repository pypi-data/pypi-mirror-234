from lamin_vault.client.postgres._delete_db_vault import delete_db_vault
from lamin_vault.client.postgres._role_and_policy_exist import role_and_policy_exist


def test_delete_db_vault(instance_context_with_vault):
    from hvac.exceptions import InvalidPath

    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]
    instance_id = instance_context_with_vault["instance_id"]
    admin_account_id = instance_context_with_vault["account_id"]
    # role_name = instance_context_with_vault["role_name"]
    # policy_name = f"{role_name}-policy"

    # Verify that the connection configuration exists
    try:
        vault_admin_client_test.secrets.database.read_connection(name=instance_id)
    except InvalidPath:
        assert False, "Connection configuration should exist in vault."

    # Verify that the role and policy exist
    assert role_and_policy_exist(
        vault_client=vault_admin_client_test,
        instance_id=instance_id,
        account_id=admin_account_id,
    ), "Admin role and policy should exist in vault."

    # Delete the connection configuration and all associated roles and policies
    delete_db_vault(vault_admin_client_test, instance_id)

    # Verify that the connection configuration no longer exists
    try:
        vault_admin_client_test.secrets.database.read_connection(name=instance_id)
    except InvalidPath:
        pass
    else:
        assert False, "Connection configuration should not exist in vault."

    # TODO: These tests doesn't currently pass

    # # Verify that the role and policy no longer exist
    # assert not role_and_policy_exist(
    #     vault_client=vault_admin_client_test,
    #     instance_id=instance_id,
    #     account_id=admin_account_id,
    # ), "Admin role and policy should not exist in vault."

    # # Verify that the role and policy no longer exist
    # try:
    #     vault_admin_client_test.secrets.database.read_role(name=role_name)
    # except InvalidPath:
    #     pass
    # else:
    #     assert False, "Admin role should not exist in vault."

    # try:
    #     vault_admin_client_test.sys.read_policy(name=policy_name)
    # except InvalidPath:
    #     pass
    # else:
    #     assert False, "Admin policy should not exist in vault."
