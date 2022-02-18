from typing import Tuple
from sqlalchemy import create_engine
from core.config import settings


def db_uri_info() -> Tuple[str, bool]:
    """
    This function return information about conection to database based in the settings file.

    @:returns: Database URI and if is an SQLITE database or not.
    """
    if settings.PRODUCTION:
        if settings.MASTER:
            return settings.SQLALCHEMY_DATABASE_URI_MSSQL_MASTER, False
        return settings.SQLALCHEMY_DATABASE_URI_MSSQL_PROD_CRM, False

    if settings.SQLITE:
        return settings.SQLALCHEMY_DATABASE_URI_SQLITE, True

    if settings.MASTER:
            return settings.SQLALCHEMY_DATABASE_URI_MSSQL_DEV_MASTER, False
    return settings.SQLALCHEMY_DATABASE_URI_MSSQL_DEV_CRM, False


db_uri, is_sqlite = db_uri_info()
print(db_uri, is_sqlite)
if is_sqlite:
    engine = create_engine(db_uri, connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_uri)