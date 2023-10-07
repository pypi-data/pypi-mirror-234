def delete_db_role(vault_admin_client, instance_id, account_id):
    role_name = f"{instance_id}-{account_id}-db"
    policy_name = f"{role_name}-policy"
    connection_config_path = f"database/config/{instance_id}"
    delete_db_role_base(
        vault_admin_client, connection_config_path, role_name, policy_name
    )


def delete_db_role_base(
    vault_admin_client, connection_config_path, role_name, policy_name
):
    # Delete role
    vault_admin_client.secrets.database.delete_role(name=role_name)

    # Delete policy
    vault_admin_client.sys.delete_policy(name=policy_name)

    # Update allowed_roles of connection configuration

    current_config = vault_admin_client.read(connection_config_path)["data"]
    allowed_roles = set(current_config.get("allowed_roles", []))
    allowed_roles.discard(role_name)
    vault_admin_client.write(
        connection_config_path,
        allowed_roles=list(allowed_roles),
    )
