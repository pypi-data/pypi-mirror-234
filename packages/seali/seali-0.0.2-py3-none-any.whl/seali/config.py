"""Store configuration."""
from __future__ import annotations

import logging
import pathlib

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
cwd_config = cwd / "config.yml"

home_config = home / ".config" / "seali.yml"
config_dir = home / ".config"
config_dir.mkdir(exist_ok=True)
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent.parent


class Path:
    module = module_path
    repo = repo_path
    test_data = repo / "tests" / "data"


class Settings(BaseSettings):
    """SeaLI settings object.

    Attributes:
        url: URL of the GDataSea server.
    """

    url: str = "http://localhost:3131"

    model_config = SettingsConfigDict(
        validation=True,
        arbitrary_types_allowed=True,
        env_prefix="seali_",
        env_nested_delimiter="_",
    )

    @classmethod
    def from_config(cls) -> Settings:
        """Load settings from YAML config file.
        Recursively search for a `gfconfig.yml` file in the current working directory.
        """
        path = cwd

        while path.parent != path:
            path_config = path / "seali.yml"
            if path_config.is_file():
                logger.info(f"Loading settings from {path_config}")
                return Settings(**yaml.safe_load(path_config.read_text()))
            path = path.parent
        return Settings()


PATH = Path()
CONF = Settings.from_config()

__all__ = ["PATH", "CONF"]
if __name__ == "__main__":
    print(CONF.url)
    print(PATH.test_data)
