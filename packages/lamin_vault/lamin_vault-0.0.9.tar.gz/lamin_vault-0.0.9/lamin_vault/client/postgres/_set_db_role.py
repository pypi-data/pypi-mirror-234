from lamin_vault.client.postgres._create_or_update_role_and_policy_db import (
    create_or_update_role_and_policy_db,
    set_read_credentials_policy,
    update_allowed_roles,
)


def set_admin_db_role(vault_admin_client, instance_id, account_id):
    admin_role_creation_statements = [
        "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL"
        " '{{expiration}}';",
        'GRANT CREATE ON SCHEMA public TO "{{name}}";',
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO"
        ' "{{name}}";',
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE"
        ' ON TABLES TO "{{name}}";',
        'GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO "{{name}}";',
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON"
        ' SEQUENCES TO "{{name}}";',
    ]
    create_or_update_role_and_policy_db(
        vault_admin_client, instance_id, account_id, admin_role_creation_statements
    )


def set_write_db_role(vault_admin_client, instance_id, account_id):
    write_role_creation_statements = [
        "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL"
        " '{{expiration}}';",
        'GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO "{{name}}";',
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON"
        ' TABLES TO "{{name}}";',
        'GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO "{{name}}";',
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON"
        ' SEQUENCES TO "{{name}}";',
    ]
    create_or_update_role_and_policy_db(
        vault_admin_client, instance_id, account_id, write_role_creation_statements
    )


def set_read_db_role(vault_admin_client, instance_id, account_id):
    read_role_creation_statements = [
        "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL"
        " '{{expiration}}';",
        'GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}";',
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO"
        ' "{{name}}";',
    ]
    create_or_update_role_and_policy_db(
        vault_admin_client, instance_id, account_id, read_role_creation_statements
    )


def set_public_read_db_role(vault_admin_client, instance_id):
    public_read_role_creation_statements = [
        "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}';",
        'GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}";',
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO"
        ' "{{name}}";',
    ]
    role_name = f"{instance_id}-public-read-db"

    # Create or update role
    vault_admin_client.secrets.database.create_role(
        name=role_name,
        db_name=str(instance_id),
        creation_statements=public_read_role_creation_statements,
        default_ttl="0",
        max_ttl="0",
    )

    set_read_credentials_policy(vault_admin_client, role_name)
    update_allowed_roles(vault_admin_client, role_name, instance_id)
