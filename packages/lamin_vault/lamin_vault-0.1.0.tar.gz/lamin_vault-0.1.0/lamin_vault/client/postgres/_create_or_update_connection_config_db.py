def create_or_update_connection_config_db(
    vault_admin_client,
    instance_id,
    db_host,
    db_port,
    db_name,
    vault_db_username,
    vault_db_password,
):
    vault_admin_client.secrets.database.configure(
        name=instance_id,
        plugin_name="postgresql-database-plugin",
        allowed_roles=[],
        connection_url=f"postgresql://{{{{username}}}}:{{{{password}}}}@{db_host}:{db_port}/{db_name}?sslmode=disable",  # noqa
        username=vault_db_username,
        password=vault_db_password,
        password_authentication="scram-sha-256",
    )
