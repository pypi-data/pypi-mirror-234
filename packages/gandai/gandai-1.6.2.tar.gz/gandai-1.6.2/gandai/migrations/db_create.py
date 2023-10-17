from pathlib import Path

import sqlalchemy

from gandai.db import connect_with_connector

SQL_DIR = Path(__file__).parent / "sql"


def create_db():
    db = connect_with_connector()

    with open(f"{SQL_DIR}/schema.sql", "r") as f:
        statement = sqlalchemy.text(f.read())

    with db.connect() as conn:
        conn.execute(statement)
        conn.commit()


if __name__ == "__main__":
    create_db()
