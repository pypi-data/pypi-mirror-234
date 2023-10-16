from googleapiclient.discovery import build
import gandai as ts
import pandas as pd

def page_one(q: str) -> pd.DataFrame:
    service = build(
        "customsearch",
        "v1",
        developerKey=ts.secrets.access_secret_version("GOOGLE_SEARCH_KEY"),
    )
    results = service.cse().list(q=q, cx="12cb7a511cc804eb0").execute()
    return pd.DataFrame(results["items"])