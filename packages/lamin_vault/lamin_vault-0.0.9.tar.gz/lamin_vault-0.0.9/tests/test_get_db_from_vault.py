import psycopg2

from lamin_vault.client.postgres._get_db_from_vault import get_db_from_vault


def test_get_db_from_vault(instance_context_with_vault):
    vault_client_test = instance_context_with_vault["vault_client_test"]
    db_dsn_admin = instance_context_with_vault["db_dsn"]
    role_name = instance_context_with_vault["role_name"]
    db_dsn = get_db_from_vault(
        vault_client=vault_client_test,
        scheme="postgresql",
        host=db_dsn_admin.db.host,
        port=db_dsn_admin.db.port,
        name=db_dsn_admin.db.database,
        role=role_name,
    )

    try:
        connection = psycopg2.connect(dsn=db_dsn)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert (
            result[0] == 1
        ), "Should be able to execute a query with the obtained credentials."
    finally:
        # Close the connection and cursor
        cursor.close()
        connection.close()
