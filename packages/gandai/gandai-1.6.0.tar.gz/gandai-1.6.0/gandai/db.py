import os

import pg8000
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

from gandai.secrets import access_secret_version


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    ## Connect to Dev DB
    if os.getenv("LOCAL_DB", False):
        print("📀 connecting to local db")
        return sqlalchemy.create_engine("postgresql://localhost:5432/postgres")

    connector = Connector()
    instance_connection_name = access_secret_version("INSTANCE_CONNECTION_NAME")
    db_pass = access_secret_version("DB_PASS")
    print(instance_connection_name)

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=os.getenv("DB_USER", "postgres"),
            password=db_pass,
            db=os.getenv("DB_NAME", "postgres"),
            ip_type=IPTypes.PUBLIC,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,  # 30 seconds
        pool_recycle=1800,  # 30 minutes
    )
    return pool
