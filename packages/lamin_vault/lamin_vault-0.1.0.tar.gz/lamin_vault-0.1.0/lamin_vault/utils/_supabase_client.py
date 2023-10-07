from contextlib import contextmanager

from lamin_vault.utils.connector import connect_hub, connect_hub_with_auth


class SbClientFromAccesToken:
    def __init__(self, access_token) -> None:
        self.access_token = access_token

    @contextmanager
    def connect(self):
        supabase_client = connect_hub_with_auth(access_token=self.access_token)
        try:
            yield supabase_client
        finally:
            supabase_client.auth.sign_out()


class SbClientAnonymous:
    @contextmanager
    def connect(self):
        supabase_client = connect_hub()
        try:
            yield supabase_client
        finally:
            supabase_client.auth.sign_out()


# class SbClientAdmin:
#    @contextmanager
#    def connect(self):
#        supabase_client = connect_hub_with_service_role()
#        try:
#            yield supabase_client
#        finally:
#            supabase_client.auth.sign_out()
#
