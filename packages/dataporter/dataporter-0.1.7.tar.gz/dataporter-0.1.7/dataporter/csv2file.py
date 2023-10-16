import pandas as pd
from loguru import logger
from typing import Optional, List, Literal, Iterable, TypeAlias
from fire import Fire
from dataporter.utils import exec_multi_expr

FileWriteMode: TypeAlias = Literal["a", "w", "x", "at", "wt", "xt", "ab", "wb", "xb", "w+", "w+b", "a+", "a+b"]


def write_file(
    trunk_df: Iterable[pd.DataFrame],
    mode: FileWriteMode,
    file_type: Literal["csv", "json"],
    pandas_exprs: List[str] | None,
    debug: bool,
    header: bool = True,
    names: List[str] | None = None,
    **pandas_kwargs,
):
    for i, df in enumerate(trunk_df):
        if names:
            df = df.rename(dict(zip(df.columns, names)), axis=1)
            if i == 0:
                logger.info(f"will rename {df.columns} to {names}")

        if pandas_exprs:
            df = exec_multi_expr(df, pandas_exprs, debug=debug)
        df: pd.DataFrame
        if mode.startswith("w") and i == 0:
            if file_type == "csv":
                df.to_csv(**pandas_kwargs, mode=mode, header=header)
            else:
                df.to_json(**pandas_kwargs, mode=mode)  # type: ignore
        else:
            if file_type == "csv":
                df.to_csv(**pandas_kwargs, mode="a", header=False)
            else:
                df.to_json(**pandas_kwargs, mode="a")


def csv2file(
    read_filename: str,
    write_filename: str,
    read_names: Optional[List[str]] = None,
    read_sep: str = ",",
    read_quotechar: str = '"',
    read_escapechar: Optional[str] = None,
    read_lineterminator: Optional[str] = None,
    header: List[int] | Literal["infer"] | None = "infer",
    write_header: bool = True,
    write_names: Optional[List[str]] = None,
    write_mode: FileWriteMode = "w",
    write_lines: bool = False,
    write_orient: Literal["columns", "split", "records", "values", "table"] = "records",
    write_date_unit: Literal["ms", "s", "us", "ns"] = "ms",
    write_date_format: Literal["epoch", "iso"] = "iso",
    sep: str = ",",
    index: bool = False,
    quotechar: str = '"',
    escapechar: Optional[str] = None,
    lineterminator: Optional[str] = None,
    chunk_size: Optional[int] = None,
    pandas_exprs: List[str] | None = None,
    debug: bool = False,
):
    """
    convert csv to csv/json file.

    :param read_filename: source csv filename.
    :param write_filename: target csv/json filename, please specify the ext in filename.
    :param read_names: source csv column names, a list e.g. `a,b,c,d`, defaults to None.
    :param read_sep: source csv sep defaults to ",".
    :param read_quotechar: source csv quotechar, defaults to '"'.
    :param read_escapechar: source csv escapechar, defaults to '"'.
    :param read_lineterminator: source csv lineterminator, defaults to '\n;
    :param header: source csv, header parameter in pandas read_csv, defaults to "infer".
    :param write_header: if write header to target csv.
    :param write_names: target csv columns, a list e.g. `a,b,c,d`, defaults to None.
    :param write_mode: how to write the csv, same as mode in open().
    :param write_lines: json format only, default True, If ‘orient’ is ‘records’ write out line-delimited json format. Will throw ValueError if incorrect ‘orient’ since others are not list-like.
    :param write_orient: json format only, reference: pandas to_json write_orient, default `records`.
    :param write_date_unit: "ms", "s", "us", "ns" default "ms".
    :param write_date_format: "epoch" or "iso" default "iso".
    :param sep: target csv sep, defaults to ",".
    :param index: should write index(linenumber) to target csv, defaults to False.
    :param quotechar: target csv quotechar, defaults to '"'.
    :param escapechar: target csv escapechar, defaults to '"'.
    :param lineterminator: target csv lineterminator, defaults to '\n'.
    :param chunk_size: read&write chunk size, use less memory, defaults to None
    :param pandas_exprs: exec multiple pandas expr in order, e.g.--pandas_exprs="['df.drop([\"xxxx\"], axis=1)','expr2 xxx']".
    :param debug: if debug mod on, will print every result after exec pandas exprs.
    """
    file_type: Literal["csv", "json"] = write_filename.lower().split(".")[-1]  # type: ignore
    assert file_type in ("csv", "json"), f"not support file type: {file_type}"
    if chunk_size is None:
        df = pd.read_csv(
            read_filename,
            sep=read_sep,
            names=read_names,
            header=header,
            quotechar=quotechar,
            escapechar=read_escapechar,
            lineterminator=read_lineterminator,
        )

        if write_names:
            logger.info(f"will rename {df.columns} to {write_names}")
            df = df.rename(dict(zip(df.columns, write_names)), axis=1)

        if pandas_exprs:
            df = exec_multi_expr(df, pandas_exprs, debug=debug)
        if file_type == "csv":
            df.to_csv(
                write_filename,
                index=index,
                sep=sep,
                quotechar=quotechar,
                escapechar=escapechar,
                mode=write_mode,
                header=write_header,
            )
        elif file_type == "json":
            df.to_json(
                write_filename,
                orient=write_orient,
                date_format=write_date_format,
                date_unit=write_date_unit,
                lines=write_lines,
            )
        else:
            raise ValueError(f"unsupported file type: {write_filename}")

    else:
        df = pd.read_csv(
            read_filename,
            sep=read_sep,
            chunksize=chunk_size,
            names=read_names,
            header=header,
            quotechar=read_quotechar,
            escapechar=read_escapechar,
            lineterminator=read_lineterminator,
            iterator=True,
        )
        if file_type == "csv":
            write_file(
                df,
                file_type=file_type,
                pandas_exprs=pandas_exprs,
                debug=debug,
                header=write_header,
                mode=write_mode,
                path_or_buf=write_filename,
                sep=sep,
                names=write_names,
                index=index,
                chunksize=chunk_size,
                quotechar=quotechar,
                escapechar=escapechar,
                lineterminator=lineterminator,
            )
        else:
            write_file(
                df,
                file_type=file_type,
                pandas_exprs=pandas_exprs,
                debug=debug,
                mode=write_mode,
                path_or_buf=write_filename,
                orient=write_orient,
                date_format=write_date_format,
                date_unit=write_date_unit,
                lines=write_lines,
            )


def main():
    Fire(csv2file)


if __name__ == "__main__":
    main()
