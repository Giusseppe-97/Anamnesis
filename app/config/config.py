import os
import secrets
from typing import List
from decouple import config as config_env
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # GENERAL SETTINGS
    API_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    SERVER_NAME: str = ""
    SERVER_HOST: AnyHttpUrl = None
    PRODUCTION_CORS_ORIGINS: List[AnyHttpUrl] = ['http://app.anamnesia.com', 'https://app.anamnesia.com',
                                                 "http://localhost", "http://localhost:8080", "http://localhost:8082"]
    DEVELOPMENT_CORS_ORIGINS: List[str] = ['http://app.anamnesia.com', 'https://app.anamnesia.com',
                                           "http://localhost", "http://localhost:8080", "http://localhost:8082"]
    PROJECT_NAME: str = "BlackWood-API-Web"

    # PROYECT
    PRODUCTION: bool = config_env("PRODUCTION_MODE") == 'True'
    CORS_ALLOW_CUSTOM_ORIGINS_FLAG: bool = config_env("CORS_ALLOW_CUSTOM_ORIGINS_FLAG") == 'True'  # TODO: ELIMINAR ESTO

    # DATA BASE SQLITE MODE
    SQLITE: bool = config_env("LOCAL_DB") == 'True'

    # AWS
    AWS_ACCESS_KEY_ID = config_env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config_env("AWS_SECRET_ACCESS_KEY")
    IMPORT_TOOL_BUCKET_NAME = config_env("S3_IMPORT_TOOL_BUCKET_NAME_DEV")
    if PRODUCTION:
        IMPORT_TOOL_BUCKET_NAME = config_env("S3_IMPORT_TOOL_BUCKET_NAME")

    # STORAGE
    REMOTE_STORAGE: bool = config_env("REMOTE_STORAGE") == 'True'

    STORAGE_PATH: str = os.path.join(os.getcwd(), 'storage')
    STORAGE_S3_PATH: str = f's3://{IMPORT_TOOL_BUCKET_NAME}'
    LOCAL_IMPORT_TOOL_PATH: str = os.path.join(STORAGE_PATH, 'import_tool')
    LOCAL_IMPORT_TOOL_TEMP_PATH: str = os.path.join(LOCAL_IMPORT_TOOL_PATH, 'temp')

    # SQLITE DATABASE
    SQLALCHEMY_DATABASE_URI_SQLITE: str = os.path.join("sqlite:///", 'storage/db/database.db')

    # SQLMICROSOFTSERVER DATABASE
    USER: str = config_env("USER")
    PASSWORD: str = config_env("PASSWORD")
    MASTER : bool = config_env("MASTER") == 'True'

    SQLALCHEMY_DATABASE_URI_MSSQL_DEV_CRM: str = f"mssql+pyodbc://{USER}:{PASSWORD}@blackwoodbd" \
                                                 f".c3pkflq6wzsh.us-east-1.rds.amazonaws.com:1433/Dev_BlackWoodCRM" \
                                                 f"?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_DATABASE_URI_MSSQL_PROD_CRM: str = f"mssql+pyodbc://{USER}:{PASSWORD}@blackwoodbd" \
                                                  f".c3pkflq6wzsh.us-east-1.rds.amazonaws.com:1433/BlackWoodCRM" \
                                                  f"?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_DATABASE_URI_MSSQL_MASTER: str = f"mssql+pyodbc://{USER}:{PASSWORD}@blackwoodbd" \
                                                f".c3pkflq6wzsh.us-east-1.rds.amazonaws.com:1433/BlackWood" \
                                                f"?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_DATABASE_URI_MSSQL_DEV_MASTER: str = f"mssql+pyodbc://{USER}:{PASSWORD}@blackwoodbd" \
                                                f".c3pkflq6wzsh.us-east-1.rds.amazonaws.com:1433/DevBlackWood" \
                                                f"?driver=ODBC+Driver+17+for+SQL+Server"


settings = Settings()
