import os
from typing import Optional

import yaml
from pydantic import BaseSettings


class MongoConfig(BaseSettings):
    host: str
    port: str
    driver: str
    username: str
    password: str
    db_name: str


class Settings(BaseSettings):
    mongo: Optional[MongoConfig]

    @property
    def mongo_url(self) -> str:
        return (
            f"{self.mongo.driver}://{self.mongo.username}:"
            f"{self.mongo.password}@{self.mongo.host}"
            f":{self.mongo.port}/{self.mongo.db_name}?authSource=admin"
        )


def setup_settings() -> Settings:
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../../config.yaml",
    )
    with open(path, "r") as f:
        raw_config = yaml.safe_load(f)

    return Settings(
        mongo=MongoConfig(
            host=raw_config["mongo"]["host"],
            port=int(raw_config["mongo"]["port"]),
            driver=raw_config["mongo"]["driver"],
            username=raw_config["mongo"]["username"],
            password=raw_config["mongo"]["password"],
            db_name=raw_config["mongo"]["db_name"],
        ),
    )


settings = setup_settings()
