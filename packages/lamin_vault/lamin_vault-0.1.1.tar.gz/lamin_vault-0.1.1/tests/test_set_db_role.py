import psycopg2

from lamin_vault.client.postgres._get_db_from_vault import get_db_from_vault
from lamin_vault.client.postgres._set_db_role import (
    set_admin_db_role,
    set_public_read_db_role,
    set_read_db_role,
    set_write_db_role,
)


def test_set_public_read_role(instance_context_with_vault):
    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]
    vault_client_test = instance_context_with_vault["vault_client_test"]
    db_dsn_admin = instance_context_with_vault["db_dsn"]
    instance_id = instance_context_with_vault["instance_id"]

    set_public_read_db_role(vault_admin_client_test, instance_id)
    role_name = f"{instance_id}-public-read-db"
    db_dsn = get_db_from_vault(
        vault_client=vault_client_test,
        scheme="postgresql",
        host=db_dsn_admin.db.host,
        port=db_dsn_admin.db.port,
        name=db_dsn_admin.db.database,
        role=role_name,
    )

    _check_read_role(db_dsn, db_dsn_admin, "test_table_public_read")


def test_set_read_role(instance_context_with_vault):
    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]
    vault_client_test = instance_context_with_vault["vault_client_test"]
    db_dsn_admin = instance_context_with_vault["db_dsn"]
    instance_id = instance_context_with_vault["instance_id"]
    admin_account_id = instance_context_with_vault["account_id"]

    set_read_db_role(vault_admin_client_test, instance_id, admin_account_id)
    role_name = instance_context_with_vault["role_name"]
    db_dsn = get_db_from_vault(
        vault_client=vault_client_test,
        scheme="postgresql",
        host=db_dsn_admin.db.host,
        port=db_dsn_admin.db.port,
        name=db_dsn_admin.db.database,
        role=role_name,
    )

    _check_read_role(db_dsn, db_dsn_admin, "test_table_read")


def _check_read_role(db_dsn, db_dsn_admin, table_name):
    # Create table with the admin connection string
    connection_admin = psycopg2.connect(dsn=str(db_dsn_admin.db))
    cursor_admin = connection_admin.cursor()
    cursor_admin.execute(
        psycopg2.sql.SQL(
            f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, col VARCHAR(255));"
        )
    )
    cursor_admin.execute(
        psycopg2.sql.SQL(f"INSERT INTO {table_name} (col) VALUES ('value');")
    )
    connection_admin.commit()

    # Use connection string generated for read role
    connection = psycopg2.connect(dsn=db_dsn)
    cursor = connection.cursor()

    # Select data
    cursor.execute(psycopg2.sql.SQL(f"SELECT * FROM {table_name} WHERE id = 1;"))
    result = cursor.fetchone()
    assert result is not None, "Read role should be able to select data"

    # Attempt to insert data
    try:
        cursor.execute(
            psycopg2.sql.SQL(f"INSERT INTO {table_name} (col) VALUES ('value');")
        )
    except psycopg2.errors.InsufficientPrivilege:
        pass
    else:
        assert False, "Read role should not be able to insert data"

    # Attempt to update data
    try:
        cursor.execute(
            psycopg2.sql.SQL(f"UPDATE {table_name} SET col = 'new_value' WHERE id = 1;")
        )
    except psycopg2.errors.InFailedSqlTransaction:
        pass
    else:
        assert False, "Read role should not be able to update data"

    # Attempt to delete data
    try:
        cursor.execute(psycopg2.sql.SQL(f"DELETE FROM {table_name} WHERE id = 1;"))
    except psycopg2.errors.InFailedSqlTransaction:
        pass
    else:
        assert False, "Read role should not be able to delete data"

    # Attempt to create table
    try:
        cursor.execute(
            psycopg2.sql.SQL(
                f"CREATE TABLE {table_name}_2 (id SERIAL PRIMARY KEY, col"
                " VARCHAR(255));"
            )
        )
    except psycopg2.errors.InFailedSqlTransaction:
        pass
    else:
        assert False, "Read role should not be able to create table"

    cursor.close()
    connection.close()
    cursor_admin.execute(psycopg2.sql.SQL(f"DROP TABLE {table_name};"))
    cursor_admin.close()
    connection.close()


def test_set_write_role(instance_context_with_vault):
    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]
    vault_client_test = instance_context_with_vault["vault_client_test"]
    db_dsn_admin = instance_context_with_vault["db_dsn"]
    instance_id = instance_context_with_vault["instance_id"]
    admin_account_id = instance_context_with_vault["account_id"]

    set_write_db_role(vault_admin_client_test, instance_id, admin_account_id)
    role_name = instance_context_with_vault["role_name"]
    db_dsn = get_db_from_vault(
        vault_client=vault_client_test,
        scheme="postgresql",
        host=db_dsn_admin.db.host,
        port=db_dsn_admin.db.port,
        name=db_dsn_admin.db.database,
        role=role_name,
    )

    # Create table with the admin connection string
    connection_admin = psycopg2.connect(dsn=str(db_dsn_admin.db))
    cursor_admin = connection_admin.cursor()
    cursor_admin.execute(
        psycopg2.sql.SQL(
            "CREATE TABLE test_table_write (id SERIAL PRIMARY KEY, col VARCHAR(255));"
        )
    )
    connection_admin.commit()

    # Use connection string generated for write role
    connection = psycopg2.connect(dsn=db_dsn)
    cursor = connection.cursor()

    # Insert data
    cursor.execute(
        psycopg2.sql.SQL("INSERT INTO test_table_write (col) VALUES ('value');")
    )

    # Select data
    cursor.execute(psycopg2.sql.SQL("SELECT * FROM test_table_write WHERE id = 1;"))
    result = cursor.fetchone()
    assert result is not None, "Write role should be able to select data"

    # Update data
    cursor.execute(
        psycopg2.sql.SQL("UPDATE test_table_write SET col = 'new_value' WHERE id = 1;")
    )

    # Attempt to delete data
    try:
        cursor.execute(psycopg2.sql.SQL("DELETE FROM test_table_write WHERE id = 1;"))
    except psycopg2.errors.InsufficientPrivilege:
        pass
    else:
        assert False, "Write role should not be able to delete data"

    # Attempt to create table
    try:
        cursor.execute(
            psycopg2.sql.SQL(
                "CREATE TABLE test_table_write_2 (id SERIAL PRIMARY KEY, col"
                " VARCHAR(255));"
            )
        )
    except psycopg2.errors.InFailedSqlTransaction:
        pass
    else:
        assert False, "Write role should not be able to create table"

    cursor.close()
    connection.close()
    cursor_admin.execute(psycopg2.sql.SQL("DROP TABLE test_table_write;"))
    cursor_admin.close()
    connection_admin.close()


def test_set_admin_role(instance_context_with_vault):
    vault_admin_client_test = instance_context_with_vault["vault_admin_client_test"]
    vault_client_test = instance_context_with_vault["vault_client_test"]
    db_dsn_admin = instance_context_with_vault["db_dsn"]
    instance_id = instance_context_with_vault["instance_id"]
    admin_account_id = instance_context_with_vault["account_id"]

    set_admin_db_role(vault_admin_client_test, instance_id, admin_account_id)
    role_name = instance_context_with_vault["role_name"]
    db_dsn = get_db_from_vault(
        vault_client=vault_client_test,
        scheme="postgresql",
        host=db_dsn_admin.db.host,
        port=db_dsn_admin.db.port,
        name=db_dsn_admin.db.database,
        role=role_name,
    )

    # Use connection string generated for admin role
    connection = psycopg2.connect(dsn=db_dsn)
    cursor = connection.cursor()

    # Create table
    cursor.execute(
        psycopg2.sql.SQL(
            "CREATE TABLE test_table_admin (id SERIAL PRIMARY KEY, col VARCHAR(255));"
        )
    )

    # Insert data
    cursor.execute(
        psycopg2.sql.SQL("INSERT INTO test_table_admin (col) VALUES ('value');")
    )

    # Update data
    cursor.execute(
        psycopg2.sql.SQL("UPDATE test_table_admin SET col = 'new_value' WHERE id = 1;")
    )

    # Select data
    cursor.execute(psycopg2.sql.SQL("SELECT * FROM test_table_admin WHERE id = 1;"))
    result = cursor.fetchone()
    assert result is not None, "Admin should be able to select data"

    # Delete data
    cursor.execute(psycopg2.sql.SQL("DELETE FROM test_table_admin WHERE id = 1;"))

    cursor.execute(psycopg2.sql.SQL("DROP TABLE test_table_admin;"))
    cursor.close()
    connection.close()
