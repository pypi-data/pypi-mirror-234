from lamin_vault.utils._supabase_client import SbClientFromAccesToken


def create_instance_admin_token_from_jwt(
    vault_client_approle, access_token, instance_id
):
    # Verify JWT token and check user is admin
    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        supabase_client.auth.get_user(access_token)
        # TODO: check user is an instance admin
        create_admin_policy(vault_client_approle, instance_id)

    # Create token to access vault
    created_token_response = vault_client_approle.auth.token.create(
        policies=[f"{instance_id}-admin-db-policy"], ttl="1h", wrap_ttl="1m"
    )
    vault_token = created_token_response["wrap_info"]["token"]

    return vault_token


def create_admin_policy(vault_client_approle, instance_id):
    policy = f"""
    path "database/config/{instance_id}" {{
      capabilities = ["create", "update", "read", "delete"]
    }}

    path "database/roles/{instance_id}-*" {{
      capabilities = ["create", "update", "read", "delete", "list"]
    }}

    path "database/roles/" {{
      capabilities = ["list"]
    }}

    path "database/creds/{instance_id}-*" {{
      capabilities = ["read"]
    }}

    path "sys/policy/{instance_id}-*" {{
      capabilities = ["create", "read", "update", "delete", "list"]
    }}
    """
    vault_client_approle.sys.create_or_update_policy(
        name=f"{instance_id}-admin-db-policy", policy=policy
    )
