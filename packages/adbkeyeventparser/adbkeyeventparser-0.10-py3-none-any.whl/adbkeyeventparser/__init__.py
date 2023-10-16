import requests
from a_pandas_ex_bs4df_lite import pd_add_bs4_to_df_lite
import pandas as pd

pd_add_bs4_to_df_lite()
from PrettyColorPrinter import add_printer

add_printer(1)
import lxml


def parse_keycodes(
    url=r"https://developer.android.com/reference/android/view/KeyEvent",
):
    r"""
    Parameters:
    url (str, optional): The URL to the Android KeyEvent documentation. Default is the official Android KeyEvent documentation URL.

    Returns:
    dict: A dictionary where keys are keycodes and values are dictionaries containing information about the key, including:
        - 'as_int' (int): The key code as an integer.
        - 'as_hex' (str): The key code as a hexadecimal string.
        - 'description' (str): Description of the key.
        - 'added' (int or None): The API level at which the key was added, or None if not specified.
        - 'deprecated' (int or None): The API level at which the key was deprecated, or None if not deprecated.

    Example:
    from adbkeyeventparser import parse_keycodes
    keycodes = parse_keycodes()
    print(keycodes['KEYCODE_ENTER'])
    {'as_int': 66, 'as_hex': '0x00000042', 'description': 'Key code constant: Enter key.', 'added': 1, 'deprecated': None}

    """
    with requests.get(url) as r:
        data = r.content
    df = pd.Q_bs4_to_df_lite(data, parser="lxml", fake_header=True)
    df = df.loc[(df.aa_name == "div") & (df.aa_key == "data-version-added")]
    df["contentlen"] = df.aa_contents.str.len()
    df = df.loc[df.contentlen < 30].reset_index(drop=True)
    df = (
        df.aa_contents.apply(
            lambda q: [
                g if "Constant Value:" not in g else g.split("(")[-1].split(")")[0]
                for x in q
                if "Added in API" in (g := x.text.strip())
                or x.name in ["p", "h3"]
                or "Constant Value:" in g
            ]
        )
        .apply(lambda q: [x for x in q if x])
        .apply(lambda q: q if len(q) == 4 else pd.NA)
        .dropna()
    ).to_frame()
    df = df.aa_contents.apply(pd.Series)
    df = df.rename(columns={0: "aa_keycode", 1: "aa_api", 2: "aa_infos", 3: "aa_hex"})
    df = df.loc[df.aa_hex.str.contains("0x")]
    df.loc[:, "aa_added_in"] = df["aa_api"].str.extract(
        r"Added\s+in\s+API\s+level\s+(\d+)"
    )
    df.loc[:, "aa_deprecated_in"] = df["aa_api"].str.extract(
        r"Deprecated\s+in\s+API\s+level\s+(\d+)"
    )
    df.loc[:, "aa_key_code_int"] = df["aa_hex"].apply(lambda i: int(i, base=16))
    df = df.astype(
        {
            "aa_added_in": "Int64",
            "aa_deprecated_in": "Int64",
            "aa_key_code_int": "Int64",
        }
    )
    allkeys = {}
    for key, item in df.iterrows():
        allkeys[item.aa_keycode] = {
            "as_int": item.aa_key_code_int,
            "as_hex": item.aa_hex,
            "description": item.aa_infos,
            "added": item.aa_added_in,
            "deprecated": item.aa_deprecated_in
            if not pd.isna(item.aa_deprecated_in)
            else None,
        }
    return allkeys


