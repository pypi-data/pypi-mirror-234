import re

import pandas as pd

from gandai import query
from gandai.models import Search


def dealcloud_company_query(
    fp="/Users/parker/Development/gandai-workspace/notebooks/2023-05-13/data/Company_05132023.xlsx",
) -> pd.DataFrame:
    print("dealcloud_company_query")

    def _get_domain(url) -> str:
        url = url.replace("http://", "").replace("https://", "").replace("www.", "")
        return url.split("/")[0]

    df = pd.read_excel(fp)  # hmm why so slow, maybe just select specific columns?
    df.columns = [col.replace(" ", "_").replace(".", "").lower() for col in df.columns]
    assert "dealcloud_id" in df.columns
    df["domain"] = df["website"].dropna().apply(_get_domain)
    df["days_since_contact"] = (
        df["days_since_contact"].dropna().apply(lambda x: int(re.findall(r"\d+", x)[0]))
    )
    df = df.rename(
        columns={"company_name": "name", "business_description": "description"}
    )
    # df = (
    #     df[["dealcloud_id","name", "domain", "days_since_contact"]]
    #     .drop_duplicates(subset=["domain"])
    #     .reset_index(drop=True)
    # )
    return df


def dealcloud_engagements(fp="data/Engagement_05132023.xlsx"):
    df = pd.read_excel(fp)
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    df["dealcloud_id"] = df["dealcloud_id"].astype(str)
    assert "dealcloud_id" in df.columns
    today = pd.to_datetime("today")
    df["modified_days_ago"] = (today - pd.to_datetime(df["modified_date"])).dt.days
    date_cols = [col for col in df.columns if col.endswith("_date")]
    for col in date_cols:
        df[col] = df[col].apply(lambda x: str(x)[0:10])
    df = df.dropna(subset=["engagement_name"])  # never hit this condition
    df = df.sort_values("modified_date", ascending=False)
    df = df[
        ~df["status"].isin(
            ["Lost Pre-Mandate", "Completed Engagement", "Dead Post-Mandate"]
        )
    ].reset_index(drop=True)
    df = df[df["modified_days_ago"] < 365].reset_index(drop=True)
    return df


def migrate_engagements():
    engagements = dealcloud_engagements(
        "/Users/parker/Development/gandai-workspace/notebooks/2023-05-13/data/Engagement_05132023.xlsx"
    )
    companies = dealcloud_company_query(
        "/Users/parker/Development/gandai-workspace/notebooks/2023-05-13/data/Company_05132023.xlsx"
    )

    clients = companies[companies["name"].isin(engagements["client"])]
    clients = clients.rename(columns={"domain": "client_domain"})[
        ["name", "client_domain"]
    ]

    engagements = engagements.merge(
        clients, left_on="client", right_on="name", how="left"
    )

    for engagement in engagements.fillna("").to_dict(orient="records"):
        search = Search(
            uid=int(engagement["dealcloud_id"]),
            client_domain=engagement["client_domain"],
            label=engagement["engagement_name"],
            meta=engagement,
            inclusion={
                "country": ["USA"],
                "employees_range": [10, 100],
            },
            sort={"field": "domain", "order": "desc"},
        )
        print(search)
        query.insert_search(search)


def main():
    migrate_engagements()


if __name__ == "__main__":
    main()
