import os

from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
print(PROJECT_ID)

client = secretmanager.SecretManagerServiceClient()


def create_secret(secret_id) -> None:
    try:
        client.create_secret(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
    except Exception as e:
        print(e)


def add_secret_version(secret_id, payload) -> None:
    
    parent = client.secret_path(PROJECT_ID, secret_id)
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload.encode("UTF-8")}}
    )
    print("Added secret version: {}".format(response.name))


def access_secret_version(secret_id, version_id="latest"):
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
