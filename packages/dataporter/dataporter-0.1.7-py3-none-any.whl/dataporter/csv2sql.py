from typing import List, Literal, Optional, Any, Iterable
from loguru import logger
from fire import Fire
import pandas as pd
from sqlalchemy import create_engine, text, exc
from sqlalchemy.orm import sessionmaker
from dataporter.utils import exec_multi_expr


def insert(trunk_df: Iterable[pd.DataFrame], pandas_exprs: List[str] | None, debug: bool, sql_data_exists: Literal["append", "fail", "replace"], ignore_error: bool, table_name: str, conn, index: bool):
    for i, df in enumerate(trunk_df):
        if pandas_exprs:
            df = exec_multi_expr(df, exprs=pandas_exprs, debug=debug)
        df: pd.DataFrame
        logger.info(f"writing trunk {len(df)} line...")

        if sql_data_exists == 'append':
            # if exist strategy is append, all trunk always append
            current_data_exist = 'append'
        elif sql_data_exists == 'fail':
            # if exist strategy is fail, it should failed in first trunk
            # in later trunk, it should be append
            if i == 0:
                current_data_exist = 'fail'
            else:
                current_data_exist = 'append'
        elif sql_data_exists == 'replace':
            if i == 0:
                current_data_exist = 'replace'
            else:
                current_data_exist = 'append'
        else:
            raise ValueError(f"cannot parse current_data_exist value:{sql_data_exists}")

        with logger.catch(message="write to db error, loss chunk.", reraise=not ignore_error):
            df.to_sql(
                name=table_name,
                con=conn,
                index=index,
                if_exists=current_data_exist,
            )


def csv2sql(
    sql_uri: str,
    table_name: str,
    filename: str,
    header: List[int] | Literal["infer"] | None = "infer",
    names: Optional[List[str]] = None,
    sep: str = ",",
    index: bool = False,
    quotechar: str = '"',
    escapechar: Optional[str] = None,
    lineterminator: Optional[str] = None,
    sql_schema_file: str | None = None,
    sql_data_exists: Literal["fail", "replace", "append"] = "fail",
    read_chunk_size: Optional[int] = None,
    pandas_exprs: List[str] | None = None,
    debug: bool = False,
    ignore_error: bool = False,
    insert_in_transaction: bool = True,
    **sql_kwargs: Any
):
    """
    convert csv to sql table.
    :param sql_uri: database uri, according to sqlalchemy uri, according to sqlalchemy uri, e.g. "mysql+pymysql://username:pass@host:port/database.
    :param table_name: csv data insert table name.
    :param filename: source csv filename.
    :param header: default first line.
    :param names: specify the headers of csv file, e.g. 'a,b,c,d'.
    :param sep: sep symbol, ',' default.
    :param index: if generate index in result.
    :param quotechar: quote char, '"' default.
    :param escapechar: escape char, None default.
    :param lineterminator: line terminator, related to system ('\\n' for linux, '\\r\\n' for Windows, i.e.).
    :param sql_kwargs: other kwargs for sql, it will be pass to sqlalchemy 'create_engine' function.
    :param sql_data_exists: action on data exist in sql db, can be 'fail' or 'replace' or 'append', default 'fail'.
    :param sql_schema_file: schema on create table, default None (auto generate with no index).
    :param read_chunk_line: if csv file is large, to reduce the memory usage, read csv to memory by trunk of lines.
    :param pandas_exprs: exec multiple pandas expr in order, e.g.--pandas_exprs="['df.drop([\"xxxx\"], axis=1)','expr2 xxx']".
    :param debug: if debug mod on, will print every result after exec pandas exprs.
    :param ignore_error: if ignore sql insert error, it may cause loss chunks of data.
    :param insert_in_transaction: if insert data to db in transaction, default True.
    """
    engine = create_engine(url=sql_uri, **sql_kwargs)

    Session = sessionmaker(engine)
    # handle sql schema
    # if replace, drop table and create according to schema
    # if append or fail, try create table if not exist according to schema
    if sql_schema_file and sql_data_exists == "replace":
        logger.warning("please ensure table_name matches the sql_schema_file content, or this will cause unexpected error.")

        with open(sql_schema_file) as f:
            schema = f.read()

        with Session() as session:
            session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            logger.info("dropping table...")

            session.execute(text(schema))
            logger.info("creating table according to schema...")
            sql_data_exists = "append"
    elif sql_schema_file:
        with open(sql_schema_file) as f:
            schema = f.read()

        with Session() as session:
            try:
                session.execute(text(schema))
                logger.info("creating table according to schema(if not exist)...")
            except exc.OperationalError as e:
                if e.orig.args[0] == 1050:
                    logger.info("table already exist.")
                else:
                    raise e

    if read_chunk_size is None:
        df = pd.read_csv(
            filename,
            sep=sep,
            names=names,
            header=header,
            quotechar=quotechar,
            escapechar=escapechar,
            lineterminator=lineterminator,
        )
        if pandas_exprs:
            df = exec_multi_expr(df, exprs=pandas_exprs, debug=debug)
        with engine.begin() as conn:
            df.to_sql(
                name=table_name, con=conn, if_exists=sql_data_exists, index=index
            )
            logger.info(f"inserted {len(df)} rows")
    else:
        logger.info("converting csv to sql...")
        trunk_df = pd.read_csv(
            filename,
            sep=sep,
            chunksize=read_chunk_size,
            iterator=True,
            names=names,
            header=header,
            quotechar=quotechar,
            escapechar=escapechar,
            lineterminator=lineterminator,
        )
        if insert_in_transaction:
            with engine.begin() as conn:
                insert(
                    trunk_df=trunk_df,
                    pandas_exprs=pandas_exprs,
                    debug=debug,
                    sql_data_exists=sql_data_exists,
                    ignore_error=ignore_error,
                    table_name=table_name,
                    conn=conn,
                    index=index
                )
        else:
            with engine.connect() as conn:
                insert(
                    trunk_df=trunk_df,
                    pandas_exprs=pandas_exprs,
                    debug=debug,
                    sql_data_exists=sql_data_exists,
                    ignore_error=ignore_error,
                    table_name=table_name,
                    conn=conn,
                    index=index
                )


        logger.info("done.")


def main():
    Fire(csv2sql)


if __name__ == "__main__":
    main()
