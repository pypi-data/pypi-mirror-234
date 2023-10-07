path "database/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "database/config/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
