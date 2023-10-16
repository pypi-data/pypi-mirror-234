import pandas as pd
from typing import List
from loguru import logger


def exec_multi_expr(df: pd.DataFrame, exprs: List[str], debug: bool = False) -> pd.DataFrame:
    for expr in exprs:
        if debug:
            logger.info("exec expr: {}", expr)
        df = pd.eval(expr=expr, target=df)

        if debug:
            logger.info("result: {}", df)

    return df
