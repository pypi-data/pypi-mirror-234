def connection_config_db_exists(vault_client, instance_id):
    connection_config_path = f"database/config/{instance_id}"
    if vault_client.read(connection_config_path) is None:
        return False
    else:
        return True
