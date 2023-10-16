from gandai import query
from gandai.migrations.dealcloud import migrate_engagements
from gandai.models import Actor, Company, Event, Search


def seed_actors():
    actors = {
        "7138248581": "Parker",
        "6508620943": "Gabe",
        "9413500954": "Skye",
        "3102835279": "Chris",
        "5126571681": "Brandon",
        "5125659474": "Jack",
        "3125740050": "Jim",
        "4805706789": "Eli",
        "grata": "Grata Bot",
        "dealcloud": "DealCloud Bot",
        "chatgpt": "ChatGPT",
    }

    for key, name in actors.items():
        actor = query.insert_actor(Actor(key=key, type="research", name=name))
        print(f"Added: {actor}")


def seed_hello_world():
    search = query.insert_search(
        Search(
            uid=1,
            client_domain="parkerholcomb.com",
            label="Hello World",
            meta={"research": "Parker", "status": "In Progress"},
            inclusion={
                "keywords": [],
                "employees_range": [0, 100],
                "country": ["USA"],
            },
            exclusion={"keywords": [], "state": []},
            sort={"field": "domain", "order": "desc"},
        )
    )

    company = query.insert_company(
        Company(
            domain="grata.com",
            name="Grata",
            description="Grata is a thing.",
        )
    )

    e = query.insert_event(
        Event(
            search_uid=search.uid,
            domain=company.domain,
            actor_key="7138248581",
            type="create",
        )
    )


def main():
    seed_actors()
    seed_hello_world()


if __name__ == "__main__":
    main()
