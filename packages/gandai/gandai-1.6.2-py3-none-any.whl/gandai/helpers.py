import pandas as pd


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    return df


def clean_domain(url: str) -> str:
    # assert "." in url, "URL must contain a dot"
    url = url.lower().strip()
    url = url.replace("http://", "").replace("https://", "").replace("www.", "")
    return url.split("/")[0]

def domain_is_none(url: str) -> bool:
    return url is None or url == ""