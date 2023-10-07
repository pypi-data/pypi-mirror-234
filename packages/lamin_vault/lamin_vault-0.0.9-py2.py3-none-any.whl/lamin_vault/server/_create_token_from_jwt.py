from lamin_vault.utils._supabase_client import SbClientFromAccesToken


def create_token_from_jwt(vault_client_approle, access_token, instance_id):
    # Verify JWT token
    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        account_id = supabase_client.auth.get_user(access_token).user.id

        policies = [f"{instance_id}-{account_id}-db-policy"]

    # Create token to access vault
    created_token_response = vault_client_approle.auth.token.create(
        policies=policies, ttl="1h", wrap_ttl="1m"
    )
    vault_token = created_token_response["wrap_info"]["token"]

    return vault_token
