from typing import Optional, Any, List, TypeAlias, Literal
from fire import Fire
from loguru import logger
import pandas as pd
from sqlalchemy import create_engine


def _exec_multi_expr(df: pd.DataFrame, exprs: List[str], debug: bool = False) -> pd.DataFrame:
    for expr in exprs:
        if debug:
            logger.info("exec expr: {}", expr)
        df = pd.eval(expr=expr, target=df)

        if debug:
            logger.info("result: {}", df)

    return df


FileWriteMode: TypeAlias = Literal["a", "w", "x", "at", "wt", "xt", "ab", "wb", "xb", "w+", "w+b", "a+", "a+b"]


def sql2csv(
    sql_uri: str,
    sql: str,
    filename: str,
    index: bool = False,
    header: bool = True,
    sep: str = ",",
    quotechar: str = '"',
    escapechar: Optional[str] = None,
    lineterminator: Optional[str] = None,
    read_chunk_size: Optional[int] = None,
    write_mode: FileWriteMode = "w",
    pandas_exprs: List[str] | None = None,
    debug: bool = False,
    **sql_kwargs: Any,
):
    """
    convert sql query result to csv.
    :param sql_uri: database uri, according to sqlalchemy uri, according to sqlalchemy uri, e.g. "mysql+pymysql://username:pass@host:port/database.
    :param sql: query sql.
    :param filename: result csv filename.
    :param index: if generate index in result.
    :param header: if contains header in result.
    :param sep: sep symbol, ',' default.
    :param quotechar: quote char, '"' default.
    :param escapechar: escape char, None default.
    :param lineterminator: line terminator, related to system ('\\n' for linux, '\\r\\n' for Windows, i.e.).
    :param read_chunk_size: if sql table is large, to reduce the memory usage, read sql to memory by trunk of lines, then write to local csv.
    :param sql_kwargs: other kwargs for sql, it will be pass to sqlalchemy 'create_engine' function.
    :param write_mode: how to write the csv, same as mode in open().
    :param pandas_exprs: exec multiple pandas expr in order, e.g.--pandas_exprs="['df.drop([\"xxxx\"], axis=1)','expr2 xxx']".
    :param debug: if debug mod on, will print every result after exec pandas exprs.
    """
    engine = create_engine(url=sql_uri, **sql_kwargs)
    if read_chunk_size is None:
        with engine.begin() as conn:
            df = pd.read_sql(sql, conn)
        if pandas_exprs:
            df = _exec_multi_expr(df, exprs=pandas_exprs, debug=debug)
        df.to_csv(
            filename,
            sep=sep,
            index=index,
            header=header,
            quotechar=quotechar,
            escapechar=escapechar,
            lineterminator=lineterminator,
        )
    else:
        with engine.begin() as conn:
            trunk_df = pd.read_sql(sql, conn, chunksize=read_chunk_size)
            for i, df in enumerate(trunk_df):
                logger.info(f"reading trunk {len(df)} line...")
                if pandas_exprs:
                    df = _exec_multi_expr(df, exprs=pandas_exprs, debug=debug)
                if i == 0:
                    df.to_csv(
                        filename,
                        sep=sep,
                        index=index,
                        header=header,
                        quotechar=quotechar,
                        escapechar=escapechar,
                        lineterminator=lineterminator,
                        mode=write_mode,
                    )
                else:
                    df.to_csv(
                        filename,
                        sep=sep,
                        index=index,
                        header=False,
                        quotechar=quotechar,
                        escapechar=escapechar,
                        lineterminator=lineterminator,
                        mode="a",
                    )
        logger.info("done.")


def main():
    Fire(sql2csv)


if __name__ == "__main__":
    main()
