from pydantic import BaseSettings
# import os
# from dotenv import load_dotenv,find_dotenv

# load_dotenv(find_dotenv())
# envpass:str=os.getenv('PASS')

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_file=".env"


settings = Settings()