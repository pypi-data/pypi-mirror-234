from typing import Optional

from pydantic import BaseModel, validator
from pydantic.networks import MultiHostDsn


class LaminDsn(MultiHostDsn):
    """Custom DSN Type for Lamin.

    This class allows us to customize the allowed schemes for databases
    and also handles the parsing and building of DSN strings with the
    database name instead of URL path.
    """

    allowed_schemes = {
        "postgresql",
        # future enabled schemes
        # "snowflake",
        # "bigquery"
    }
    user_required = True
    __slots__ = ()

    @property
    def database(self):
        return self.path[1:]

    @classmethod
    def build(
        cls,
        *,
        scheme: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: str,
        port: Optional[str] = None,
        database: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        **_kwargs: str,
    ) -> str:
        return super().build(
            scheme=scheme,
            user=user,
            password=password,
            host=host,
            port=port,
            path=f"/{database}",
            query=query,
            fragment=fragment,
        )


class LaminDsnModel(BaseModel):
    db: LaminDsn

    @validator("db")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database must be provided"
        return v
