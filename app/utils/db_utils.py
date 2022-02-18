from sqlalchemy import MetaData
from sqlalchemy import Table
from db.engine import engine
metadata_obj = MetaData()


def db_table_reflection(table_name: str) -> Table:
    return Table(table_name, metadata_obj, autoload_with=engine)
