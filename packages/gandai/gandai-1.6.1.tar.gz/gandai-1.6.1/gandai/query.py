import json
from dataclasses import asdict
from typing import Any, List

from time import time
import pandas as pd
import sqlalchemy
from dacite import from_dict
from dotenv import load_dotenv


load_dotenv()

import gandai as ts

from gandai import helpers
from gandai.db import connect_with_connector
from gandai.models import Actor, Company, Event, EventType, Search

db = connect_with_connector()


### WRITES ###


def insert_event(event: Event) -> Event:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO event (search_uid, domain, actor_key, type, data) 
                VALUES(:search_uid, :domain, :actor_key, :type, :data)
                ON CONFLICT DO NOTHING
                RETURNING id
            """
        )
        obj = asdict(event)
        obj["data"] = json.dumps(obj["data"])
        result = con.execute(statement, obj)
        # print(result.first())
        _id = result.first()
        event.id = _id[0] if _id else None

        if event.type == "comment":
            con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW comment"))
        elif event.type == "rating":
            con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW rating"))
        elif event.type == "maps":
            con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW maps"))
        elif event.type == "criteria":
            con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW criteria"))
        con.commit()

    ts.trigger_process_event(event_id=event.id)
    return event


def insert_company(company: Company):
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO company (domain, name, description) 
                VALUES(:domain, :name, :description)
                ON CONFLICT DO NOTHING
            """
        )
        con.execute(statement, asdict(company))
        con.commit()
    return company  # todo this should return the id


def insert_actor(actor: Actor) -> Actor:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO actor (key, type, name) 
                VALUES(:key, :type, :name)
                ON CONFLICT DO NOTHING
            """
        )
        obj = asdict(actor)
        con.execute(statement, obj)
        con.commit()
    return actor


def insert_search(search: Search) -> Search:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO search (uid, label, meta) 
                VALUES(:uid, :label, :meta)
                ON CONFLICT DO NOTHING
            """
        )
        obj = asdict(search)
        obj["meta"] = json.dumps(obj["meta"])
        con.execute(statement, obj)
        con.commit()
    return search


# def insert_checkpoint(checkpoint: Checkpoint) -> Checkpoint:
#     with db.connect() as con:
#         statement = sqlalchemy.text(
#             """
#                 INSERT INTO checkpoint (event_id)
#                 VALUES(:event_id)
#             """
#         )
#         con.execute(statement, asdict(checkpoint))
#         con.commit()
#     return checkpoint


def insert_targets_from_domains(
    domains: List[str], search_uid: int, actor_key: str, stage: str
) -> None:
    """
    Takes in domains, inserts targets into a review stage, where they will
    try to be enriched on process event
    """

    def downstream_domains(search_uid: int, stage: str) -> set:
        STAGES = [
            "create",
            "advance",
            "validate",
            "send",
            "client_approve",
            "sync",
            "reject",
            "client_reject",
            "conflict",
            "client_conflict",
            "tmp",  # woa this is a hack, todo handle this better
        ]

        protected_stages = tuple(STAGES[STAGES.index(stage) : :])

        with db.connect() as conn:
            statement = f"""
                    SELECT distinct(domain)
                    FROM event
                    WHERE search_uid = :search_uid 
                    AND type IN {protected_stages}
                """
            result = conn.execute(
                sqlalchemy.text(statement),
                {"search_uid": search_uid},
            )
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return set(df["domain"])

    protected_domains: set = downstream_domains(search_uid=search_uid, stage=stage)

    new_domains = {helpers.clean_domain(domain) for domain in domains if "." in domain}

    domains_to_insert = list(new_domains - protected_domains)

    new_event_ids = []
    with db.connect() as con:
        with con.begin():
            for domain in domains_to_insert:
                # should these be in same transaction?
                con.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO company (domain) 
                        VALUES(:domain)
                        ON CONFLICT DO NOTHING
                        """
                    ),
                    {"domain": domain},
                )

                result = con.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO event (search_uid, domain, actor_key, type) 
                        VALUES(:search_uid, :domain, :actor_key, :type)
                        ON CONFLICT DO NOTHING
                        RETURNING id
                        """
                    ),
                    {
                        "search_uid": search_uid,
                        "actor_key": actor_key,
                        "domain": domain,
                        "type": stage,
                    },
                )

                new_event_id = result.scalar_one()
                if new_event_id is not None:
                    new_event_ids.append(new_event_id)

    for event_id in new_event_ids:
        ts.trigger_process_event(event_id=event_id)

    resp = {
        "inserted": len(domains_to_insert),
        "duplicates": len(new_domains.intersection(protected_domains)),
    }
    return resp


def insert_companies_as_targets(
    companies: List[Any], search_uid: int, actor_key: str
) -> None:
    """Takes Structured Companies (e.g. from source.find_similiar()) and inserts to Review phase"""
    print(f"Inserting {len(companies)} companies as targets...")
    existing_search_domains = unique_domains(search_uid=search_uid)["domain"].to_list()
    inserted = 0
    skipped = 0
    start = time()

    new_event_ids = []
    with db.connect() as con:
        with con.begin():
            for company in companies:
                if helpers.domain_is_none(company.get("domain")):
                    print(f"Missing domain: {company}. Skipping")
                    continue
                # elif company["domain"] in targets["domain"]:
                elif company["domain"] in existing_search_domains:
                    # print(f"Skipping {company['domain']} as already a target")
                    skipped += 1
                    continue
                else:
                    inserted += 1
                    # print(f"Adding {company['domain']} as target")

                con.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO company (domain, name, description) 
                        VALUES(:domain, :name, :description)
                        ON CONFLICT DO NOTHING
                        """
                    ),
                    {
                        "domain": company.get("domain"),
                        "name": company.get("name"),
                        "description": company.get("description"),
                    },
                )

                result = con.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO event (search_uid, domain, actor_key, type) 
                        VALUES(:search_uid, :domain, :actor_key, :type)
                        ON CONFLICT DO NOTHING
                        RETURNING id
                        """
                    ),
                    {
                        "search_uid": search_uid,
                        "actor_key": actor_key,
                        "domain": company.get("domain"),
                        "type": "create",
                    },
                )

                # Get the newly inserted ID
                new_event_id = result.scalar_one()
                if new_event_id is not None:
                    new_event_ids.append(new_event_id)

    print(new_event_ids)
    for event_id in new_event_ids:
        ts.trigger_process_event(event_id=event_id)
    print(f"Inserted {inserted}. Skipped {skipped}. Took {time() - start} seconds")


### READS ###
## returns dataframes ##


def searches_query() -> pd.DataFrame:
    statement = f"""
    SELECT 
        s.uid,
        s.label,
        s.updated,
        s.fields,
        s.meta->>'search_type' as type,
        s.meta->>'notes' as notes,
        s.meta->>'last_list' as last_list,
        s.meta->>'next_due_date' as next_due_date,
        COALESCE(s.meta->>'search_status', 'active') as search_status
    FROM search s
    ORDER BY updated
    """
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text(statement))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df["client"] = df["label"].str.split(" - ").str[0]
    return df


def mtd_validations() -> pd.DataFrame:
    statement = f"""
    WITH ranked_actors AS (
        SELECT 
            a.name as analyst,
            a.key,
            s.uid,
            COUNT(e.id) AS count,
            MAX(e.created) AS max_created,
            ROW_NUMBER() OVER (
                PARTITION BY s.uid
                ORDER BY COUNT(e.id) DESC
            ) as rn
        FROM 
            event e
        INNER JOIN 
            actor a ON a.key = e.actor_key
        INNER JOIN 
            search s ON s.uid = e.search_uid
        WHERE
            a.type = 'research' 
            AND e.type = 'validate'
            AND date_trunc('month', to_timestamp(e.created)) = date_trunc('month', current_date)
        GROUP BY 
            a.key, analyst, s.uid
    )
    SELECT 
        key as actor_key,
        analyst, 
        uid, 
        count,
        max_created
    FROM 
        ranked_actors
    WHERE 
        rn = 1;
    """
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text(statement))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df["activity"] = round(df["count"] / df["count"].max(), 2)
    return df

def average_rating_per_search_query():
    query = """
       SELECT
        search_uid,
        AVG(rating::int) AS rating_avg,
        COUNT(rating) as rating_count
    FROM rating 
    GROUP BY search_uid
    """
    return pd.read_sql(query, db)

def enriched_searches_query():
    
    searches = searches_query()
    recent_event_count = mtd_validations()
    

    df = searches.merge(
        recent_event_count, left_on="uid", right_on="uid", how="left"
    )  

    df = df.merge(
        average_rating_per_search_query(), left_on="uid", right_on="search_uid", how="left"
    )
    # df["activity"] = df["activity"].fillna(0)
    return df


def actor() -> pd.DataFrame:
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """
                SELECT * FROM actor
                """
            )
        )
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        df = df.drop(columns=["id", "created", "updated"])
        return df


def search_targets(search_uid: int):
    # arguably the most important query

    statement = """
    WITH RankedEvents AS (
        SELECT *,
            ROW_NUMBER() OVER(PARTITION BY search_uid, domain ORDER BY created DESC) AS rn
        FROM event
        WHERE 
            domain is not null
            AND search_uid = :search_uid
            AND type NOT IN ('comment','rating','criteria','update')
    )
    SELECT 
        e.search_uid, 
        e.domain, 
        e.type as stage, 
        e.created as updated, 
        a.name as updated_by, 
        c.name, 
        c.description,
        c.meta->>'ownership' as ownership, 
        c.meta->>'headquarters' as headquarters,
        c.meta->>'designation' as designation,
        c.meta->>'products' as products,
        c.meta->>'services' as services,
        c.meta->>'customers' as customers,
        c.meta->>'year_founded' as year_founded,
        c.meta->>'linkedin' as linkedin,
        c.meta,
        r.rating::int, 
        COALESCE(co.comments, '[]'::jsonb) as comments
    FROM RankedEvents e
    LEFT JOIN actor a ON e.actor_key = a.key
    LEFT JOIN company c ON e.domain = c.domain
    LEFT JOIN rating r ON e.search_uid = r.search_uid AND e.domain = r.domain
    LEFT JOIN comment co ON e.search_uid = co.search_uid AND e.domain = co.domain
    WHERE 
        e.rn = 1
    ;
    """

    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(statement),
            {"search_uid": search_uid},
        )
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_employees(meta):
        if meta.get("employees"):
            # should pull "confirmed employees"
            return int(meta["employees"])
        elif meta.get("grata_employee_estimates"):
            return meta["grata_employee_estimates"].get("count")
        else:
            return None

    def get_ownership(ownership):
        if ownership == "Bootstrapped":
            return "Private"
        elif ownership == "Investor Backed":
            return "Venture Capital"
        else:
            return ownership

    def get_state(headquarters):
        if headquarters:
            state_name = headquarters.split(",")[-1].strip()
            state_code = ts.constants.STATE_NAMES.get(state_name, "")
            return state_code
        else:
            return None

    def get_city(headquarters):
        if headquarters:
            return headquarters.split(", ")[0]
        else:
            return None

    df["employees"] = df["meta"].apply(get_employees)
    df["ownership"] = df["ownership"].apply(get_ownership)
    df["state"] = df["headquarters"].apply(get_state)
    df["city"] = df["headquarters"].apply(get_city)
    # df['year_founded'] = df['year_founded'].dropna().apply(lambda x: int(x))
    return df


def event(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM event
                WHERE search_uid = :search_uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"search_uid": search_uid})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def unique_domains(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT distinct(domain)
                FROM event
                WHERE search_uid = :search_uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"search_uid": search_uid})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


# def company() -> pd.DataFrame:
#     with db.connect() as conn:
#         statement = """
#                 SELECT *
#                 FROM company
#             """
#         result = conn.execute(sqlalchemy.text(statement))
#         df = pd.DataFrame(result.fetchall(), columns=result.keys())
#     return df


### FINDERS -> dataclass ###


def find_search(uid: int) -> ts.models.Search:
    with db.connect() as conn:
        statement = """
            SELECT 
                uid, 
                label, 
                meta, 
                fields, 
                meta->>'next_due_date' as next_due_date,
                meta->>'notes' as notes,
                COALESCE(criteria.data, '{}'::jsonb) as criteria,
                COALESCE(maps.data, '{}'::jsonb) as maps
            FROM search
            LEFT JOIN criteria ON search.uid = criteria.search_uid
            LEFT JOIN maps ON search.uid = maps.search_uid
            WHERE uid = :uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"uid": uid})
        row = result.fetchone()
        if row is None:
            return None

        obj = dict(zip(result.keys(), row))
        search = from_dict(ts.models.Search, obj)

    return search


def find_company_by_domain(domain: str) -> Company:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM company
                WHERE domain = :domain
            """
        result = conn.execute(sqlalchemy.text(statement), {"domain": domain})
        # obj = dict(zip(result.keys(), result.fetchone()))
    if result.rowcount == 0:
        return None
    else:
        obj = dict(zip(result.keys(), result.fetchone()))
        return from_dict(Company, obj)


def find_actor_by_email(email: str) -> Company:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM actor
                WHERE email = :email
            """
        result = conn.execute(sqlalchemy.text(statement), {"email": email})
        # obj = dict(zip(result.keys(), result.fetchone()))
    if result.rowcount == 0:
        return None
    else:
        obj = dict(zip(result.keys(), result.fetchone()))
        return from_dict(ts.models.Actor, obj)


def find_event_by_id(event_id: int) -> Event:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM event
                WHERE id = :event_id
            """
        result = conn.execute(sqlalchemy.text(statement), {"event_id": event_id})
        # obj = dict(zip(result.keys(), result.fetchone()))
    if result.rowcount == 0:
        return None
    else:
        obj = dict(zip(result.keys(), result.fetchone()))
        return from_dict(Event, obj)


### DELETE ###


def delete_comment(comment_id: int) -> None:
    with db.connect() as conn:
        statement = """
                DELETE FROM event
                WHERE id = :comment_id
            """
        conn.execute(sqlalchemy.text(statement), {"comment_id": comment_id})
        conn.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW comment"))
        conn.commit()


### UPDATE ###


def update_company(company: Company) -> None:
    with db.connect() as conn:
        statement = """
            UPDATE company
            SET
                uid = :uid,
                name = :name,
                description = :description,
                meta = :meta,
                updated = FLOOR(EXTRACT(EPOCH FROM NOW()))
            WHERE domain = :domain
            """

        conn.execute(
            sqlalchemy.text(statement),
            {
                "uid": company.uid,
                "name": company.name,
                "description": company.description,
                "domain": company.domain,
                "meta": json.dumps(company.meta),
            },
        )
        # conn.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW target"))
        conn.commit()


def update_search(search: Search) -> None:
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                UPDATE search
                SET
                    meta = :meta,
                    updated = FLOOR(EXTRACT(EPOCH FROM NOW()))
                WHERE uid = :uid
                """
            ),
            {
                "meta": json.dumps(search.meta),
                "uid": search.uid,
            },
        )
        conn.commit()


## DELETE ##


def reset_inbox(search_uid: int) -> None:
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                DELETE FROM event
                WHERE search_uid = :search_uid
                and type = 'create'
                """
            ),
            {"search_uid": search_uid},
        )
        conn.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW comment"))
        # conn.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW maps"))
        # conn.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW criteria"))
        conn.commit()
