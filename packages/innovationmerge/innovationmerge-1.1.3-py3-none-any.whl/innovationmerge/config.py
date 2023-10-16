# -*- coding: utf-8 -*-
from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import Optional
from io import StringIO
import io
import os
from contextlib import contextmanager
from dotenv.main import DotEnv

cwd = os.getcwd()
root_path = os.path.join(cwd, "innovationmerge")


def my_get_stream(self):
    if isinstance(self.dotenv_path, StringIO):
        yield self.dotenv_path
    elif os.path.isfile(self.dotenv_path):
        with io.open(self.dotenv_path, encoding="utf-8") as stream:
            yield stream
    else:
        if self.verbose:
            pass
        yield StringIO("")


DotEnv._get_stream = contextmanager(my_get_stream)


class Settings(BaseSettings):
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    class Config:
        ENVIRONMENT = os.getenv("ENVIRONMENT")
        env_file = os.path.join(root_path, ".env." + ENVIRONMENT)
        case_sensitive = True
        print("env_file", env_file)


class GetConfig(Settings):
    ENVIRONMENT: str = Field(None, env="ENVIRONMENT")
    HOST: str = Field(None, env="HOST")
    PORT: int = Field(None, env="PORT")
    SECRET_KEY: str = Field(None, env="SECRET_KEY")
    ALGORITHM: str = Field(None, env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(None, env="ACCESS_TOKEN_EXPIRE_MINUTES")


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        return GetConfig()


@lru_cache()
def get_configs():
    from dotenv import load_dotenv

    load_dotenv(encoding="utf-8", verbose=True)
    return FactoryConfig(Settings().ENVIRONMENT)()


configs = get_configs()
print("configs", configs.dict())
