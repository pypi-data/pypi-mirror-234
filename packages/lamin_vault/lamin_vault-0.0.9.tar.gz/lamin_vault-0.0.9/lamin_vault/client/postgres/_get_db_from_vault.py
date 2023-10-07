from lamin_vault.utils._lamin_dsn import LaminDsn


def get_db_from_vault(vault_client, scheme, host, port, name, role):
    # TODO: Fetch a user role id for postgres to replace "read"
    # something like f"{account_id}-{instance_id}-db-credentials"
    username, password = generate_db_credentials(vault_client, role)

    return LaminDsn.build(
        scheme=scheme,
        user=username,
        password=password,
        host=host,
        port=str(port),
        database=name,
    )


def generate_db_credentials(vault_client, role_name):
    credentials = vault_client.secrets.database.generate_credentials(
        name=role_name, mount_point="database"
    )

    username = credentials["data"]["username"]
    password = credentials["data"]["password"]

    return username, password
