from fire import Fire
from typing import Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from loguru import logger
import re


def change_schema_tablename(schema: str, new_table_name: str) -> str:
    return re.sub(
        r'(CREATE TABLE) (`?.*?`?) \(', 
        f"\\1 `{new_table_name}` (", 
        schema,
        flags=re.IGNORECASE
    )


def sql_schema2txt(
        sql_uri: str,
        table_name: str,
        filename: str,
        new_table_name: Optional[str] = None,
        skip_warning: bool = False,
        **sql_kwargs: Any
):
    """sql_schema2txt read db table schema and write to txt file.

    :param sql_uri: database uri, according to sqlalchemy uri, e.g. "mysql+pymysql://username:pass@host:port/database.
    :param table_name: tablename want to extract schema.
    :param skip_warning: skip safety warning.
    :param filename: txt filename, will save the result.
    :param new_table_name: this value will change the table name in schema, this feature only tested on mysql.
    :param skip_warning: if use this flag, the unsafe warning will skip.
    """
    if not skip_warning:
        logger.warning("this may cause sql injection, please ensure `table_name` is **just** tablename")
        if (input("I already known [Y]/N") or "Y").upper() != "Y":
            return

    engine = create_engine(sql_uri, **sql_kwargs)
    Session = sessionmaker(engine)
    with Session() as session:
        result = session.execute(text(f"show create table {table_name}"))
    
    with open(filename, "w") as f:
        _, schema = result.first()
        if new_table_name is not None:
            schema = change_schema_tablename(schema, new_table_name)
        f.write(schema)


def main():
    Fire(sql_schema2txt)


if __name__ == "__main__":
    main()
