import itertools
import re
from a_pandas_ex_plode_tool import pd_add_explode_tools
from functionapplydict import apply_function_dict
pd_add_explode_tools()
import pandas as pd
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed
pd_add_less_memory_more_speed()
import numpy as np
from check_if_nan import is_nan


def nestediter2df(
    it, key_prefix="level_", tmpnone="NANVALUE", fillna=pd.NA, optimize_dtypes=True
):
    r"""
    Transform a nested dictionary or iterable into a Pandas DataFrame.

    This function takes a nested dictionary or iterable and converts it into a Pandas DataFrame where each level of nesting
    is represented as a separate column. The function is designed to handle dictionaries with varying levels of nesting,
    and it can handle missing values, such as NaN or None, and fill them with the specified `tmpnone` value.

    Parameters:
    - it (dict or iterable): The input nested dictionary or iterable.
    - key_prefix (str, optional): The prefix to use for naming the columns representing each level of nesting.
      Defaults to "level_".
    - tmpnone (any, optional): The value to replace NaN or None values in the DataFrame. Defaults to "NANVALUE".
    - fillna (any, optional): The value to fill NaN values in the final DataFrame. Defaults to pd.NA.
    - optimize_dtypes (bool, optional): Whether to optimize the data types of the DataFrame columns. If True,
      it will attempt to reduce memory usage by changing data types where possible. Defaults to True.

    Returns:
    - pandas.DataFrame: A Pandas DataFrame where each level of nesting is represented as a separate column.

    Example:
        from nested2dataframe import nestediter2df
        d7 = {
            "results": [
                {
                    "end_time": "2021-01-21",
                    "key": "q1",
                    "result_type": "multipleChoice",
                    "start_time": "2021-01-21",
                    "value": ["1"],
                },
                {
                    "end_time": "2021-01-21",
                    "key": "q2",
                    "result_type": "multipleChoice",
                    "start_time": "2021-01-21",
                    "value": ["False"],
                },
                {
                    "end_time": "2021-01-21",
                    "key": "q3",
                    "result_type": "multipleChoice",
                    "start_time": "2021-01-21",
                    "value": ["3"],
                },
                {
                    "end_time": "2021-01-21",
                    "key": "q4",
                    "result_type": "multipleChoice",
                    "start_time": "2021-01-21",
                    "value": ["3"],
                },
            ]
        }

        df77 = nestediter2df(d7)
        print(df77.to_string())

        #    level_1  level_2 level_3    end_time key     result_type  start_time      0
        # 0  results        0   value  2021-01-21  q1  multipleChoice  2021-01-21      1
        # 1  results        1   value  2021-01-21  q2  multipleChoice  2021-01-21  False
        # 2  results        2   value  2021-01-21  q3  multipleChoice  2021-01-21      3
        # 3  results        3   value  2021-01-21  q4  multipleChoice  2021-01-21      3

    """
    d = {-1: it}
    d = apply_function_dict(
        d=d, fu=lambda keys, item, d: tmpnone if is_nan(item) else item
    )

    allda = []
    for x in fla_tu(d):
        s1 = pd.DataFrame(x[1][:-1]).T
        s1.columns = [f"{key_prefix}{e}" for e in s1.columns]
        s2 = pd.DataFrame([x[0]], index=[x[1][-1]]).T
        s3 = pd.concat([s1, s2], axis=1)
        allda.append(s3)
    df33 = pd.concat(allda)
    allr = []
    groupcols = [
        q[1]
        for q in (
            itertools.takewhile(
                lambda x: rf"{key_prefix}{x[0]}" == str(x[1]), enumerate(df33.columns)
            )
        )
    ]
    othercols = df33.columns[len(groupcols) :].to_list()

    for name, group in df33.groupby(groupcols, dropna=False):
        alldrs = []
        for col in othercols:
            dr = group[col].dropna().reset_index(drop=True)
            alldrs.append(dr)
        grdf = pd.concat(alldrs, axis=1).reset_index(drop=True)
        if grdf.empty:
            continue
        for g in groupcols:
            grdf.loc[:, g] = group[g].iloc[0]
        grdf = grdf[[*groupcols, *othercols]]
        allr.append(grdf)
    df34 = pd.concat(allr, ignore_index=True)
    df34 = df34.drop(columns=groupcols[0])
    levelcols = sorted(
        [x for x in df34.columns if re.match(rf"^{key_prefix}\d+$", str(x))]
    )
    valuecols = [x for x in df34.columns if x not in levelcols]
    df34 = df34[levelcols + valuecols]
    df34[df34 == tmpnone] = fillna

    if optimize_dtypes:
        df34 = df34.ds_reduce_memory_size_carefully(verbose=False)
        return df34.astype(
            {
                k: np.uint8
                for k in [
                    q
                    for q in df34.dtypes.loc[df34.dtypes == "bool"].index
                    if isinstance(q, str) and str(q).startswith(key_prefix)
                ]
            }
        )

    return df34




