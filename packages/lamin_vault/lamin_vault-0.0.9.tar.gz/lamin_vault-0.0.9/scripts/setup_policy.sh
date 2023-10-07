#!/bin/bash

export VAULT_ADDR="https://vault-cluster-public-vault-412d4780.7e7f5e61.z1.hashicorp.cloud:8200"
export VAULT_NAMESPACE="admin"

# Array of policy files
#policy_files=("my_policy1.hcl" "my_policy2.hcl" "my_policy3.hcl")
policy_files=("db-default-policy.hcl")

for policy_file in "${policy_files[@]}"; do
  # Extract policy name from file name
  policy_name="${policy_file%.*}"

  # Check if policy already exists
  vault policy read $policy_name > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Warning: Policy '$policy_name' already exists. Skipping."
  else
    # Create ACL Policy
    echo "Creating ACL policy from file $policy_file..."
    vault policy write $policy_name $policy_file 2> /dev/null
    if [ $? -ne 0 ]; then
      echo "Error: Failed to create ACL policy '$policy_name' from file '$policy_file'. Exiting."
      exit 1
    fi
  fi
done
