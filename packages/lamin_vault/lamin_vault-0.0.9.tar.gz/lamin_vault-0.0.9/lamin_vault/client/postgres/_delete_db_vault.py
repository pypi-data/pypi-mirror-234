from lamin_vault.client.postgres._delete_db_role import delete_db_role_base


def delete_db_vault(vault_admin_client, instance_id):
    connection_config_path = f"database/config/{instance_id}"

    # Delete connection configuration
    vault_admin_client.secrets.database.delete_connection(name=instance_id)

    # Get all roles
    roles = vault_admin_client.secrets.database.list_roles()

    # Delete roles and policies associated with the instance
    for role_name in roles:
        if role_name.startswith(instance_id):
            policy_name = f"{role_name}-policy"
            delete_db_role_base(
                vault_admin_client, connection_config_path, role_name, policy_name
            )
