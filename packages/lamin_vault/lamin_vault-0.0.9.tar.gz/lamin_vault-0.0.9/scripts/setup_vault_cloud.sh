#!/bin/bash

export VAULT_ADDR="https://vault-cluster-2-public-vault-91dbdbcc.459cc10d.z1.hashicorp.cloud:8200"
export VAULT_NAMESPACE="admin"
export VAULT_TOKEN="hvs.CAESIBAvLsWMfIUxVeSXF8_WhmFTmGvkYas0VzdQBrtsIFEVGicKImh2cy5uWHBrQVV2bzdtNlNKdUdyS3ZwYTRKcU0uTlJseUEQlgE"

# Log in to Vault
vault login -no-print $VAULT_TOKEN

# Enable audit logging
#vault audit enable file file_path=/vault/logs/vault_audit.log

# Install extensions
vault auth enable approle
vault secrets enable database
vault secrets enable aws
vault secrets enable gcp
vault auth enable jwt
vault auth enable userpass

# Create an app role
vault write auth/approle/role/my-role \
    secret_id_ttl=0 \
    token_num_uses=0 \
    token_ttl=20m \
    token_max_ttl=30m \
    secret_id_num_uses=0 \
    policies=hcp-root # TODO: Use specific policy

# vault read auth/approle/role/my-role/role-id
# vault write -f auth/approle/role/my-role/secret-id

# Create a new token with the default policy
#vault token create -policy=default > new_token.txt
