from lamin_vault.server._get_vault_client_approle import get_vault_approle_client


def test_get_vault_approle_client():
    client = get_vault_approle_client()
    assert client is not None, "Client should not be None"
    assert client.is_authenticated(), "Client should be authenticated"
