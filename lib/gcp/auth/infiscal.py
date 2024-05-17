import os
from dotenv import load_dotenv
from infisical_client import ClientSettings, InfisicalClient, GetSecretOptions
load_dotenv()


def get_secret(project_id, secret_name):
    ENVIRONMENT = "prod"
    
    client = InfisicalClient(ClientSettings(
    client_id=os.getenv("INFISICAL_CLIENT_ID"),
    client_secret=os.getenv("INFISCAL_CLIENT_SECRET"),
))

    name = client.getSecret(options=GetSecretOptions(
       environment=ENVIRONMENT,
       project_id=project_id,
       secret_name=secret_name
    ))

    return name.secret_value