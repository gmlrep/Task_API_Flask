import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

BD_USER = os.getenv('BD_HOSTNAME')
BD_PASSWORD = os.getenv('BD_PASSWORD')
BD_HOST = os.getenv('BD_HOST')
BD_PORT = os.getenv('BD_PORT')
BD_NAME = os.getenv('BD_NAME')


class FlaskSettings(BaseModel):
    port: int = 9000
    secret_key: str = os.getenv('SECRET_KEY')


class BdSettings(BaseSettings):
    db_url: str = f"mysql+aiomysql://{BD_USER}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}/{BD_NAME}"
    # db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db/database.db"
    echo: bool = True


class Settings(BaseSettings):
    flask_settings: FlaskSettings = FlaskSettings()
    db_settings: BdSettings = BdSettings()


settings = Settings()
