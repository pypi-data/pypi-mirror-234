def create_or_update_role_and_policy_db(
    vault_admin_client, instance_id, account_id, creation_statements
):
    role_name = f"{instance_id}-{account_id}-db"

    # Create or update role
    vault_admin_client.secrets.database.create_role(
        name=role_name,
        db_name=str(instance_id),
        creation_statements=creation_statements,
        default_ttl="1h",
        max_ttl="24h",
    )

    set_read_credentials_policy(vault_admin_client, role_name)
    update_allowed_roles(vault_admin_client, role_name, instance_id)


def set_read_credentials_policy(vault_admin_client, role_name):
    # Create or update policy to access role
    policy_name = f"{role_name}-policy"
    policy = f"""
    path "database/creds/{role_name}" {{
      capabilities = ["read"]
    }}
    """
    vault_admin_client.sys.create_or_update_policy(name=policy_name, policy=policy)


def update_allowed_roles(vault_admin_client, role_name, instance_id):
    # Update allowed_roles of connection configuration
    connection_config_path = f"database/config/{instance_id}"
    current_config = vault_admin_client.read(connection_config_path)["data"]
    allowed_roles = set(current_config.get("allowed_roles", []))
    allowed_roles.add(role_name)
    vault_admin_client.write(
        connection_config_path,
        allowed_roles=list(allowed_roles),
    )
