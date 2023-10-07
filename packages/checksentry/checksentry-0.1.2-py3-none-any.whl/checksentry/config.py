import pathlib

import pydantic
import typer

from . import sentry


class NoConfig(Exception):
    ...


class _Env(pydantic.BaseModel):
    organisation: str
    project: str
    environment: str


class _Query(pydantic.BaseModel):
    query: str
    title: str | None = None
    take: int | None = None
    sort_mode: sentry.SortMode | None = None


class Config(pydantic.BaseModel):
    sentry_token: str | None = None
    envs: dict[str, _Env]
    queries: dict[str, _Query] = pydantic.Field(default_factory=dict)


def get_config_path() -> pathlib.Path:
    app_dir = pathlib.Path(typer.get_app_dir("checksentry"))
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir / "config.json"


def get_config() -> Config:
    app_config_path = get_config_path()
    if not app_config_path.is_file():
        raise NoConfig
    with open(app_config_path) as f:
        return Config.model_validate_json(f.read())
