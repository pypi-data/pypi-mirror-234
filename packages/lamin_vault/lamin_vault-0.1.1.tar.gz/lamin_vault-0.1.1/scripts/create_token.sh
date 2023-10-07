#!/bin/bash

export VAULT_ADDR="https://vault-cluster-public-vault-412d4780.7e7f5e61.z1.hashicorp.cloud:8200"
export VAULT_NAMESPACE="admin"

vault token create -policy=db-default-policy > new_token.txt
