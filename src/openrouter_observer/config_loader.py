from pathlib import Path
from typing import Literal
from pydantic import BaseModel
import yaml
from box import Box

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "default.yaml"

class AppConfig(BaseModel):
    name: str
    version: str
    mode: Literal["dev", "prod"]
    enable_debug: bool

class ObserverConfig(BaseModel):
    log_level: str
    max_requests: int
    source: str

class Config(BaseModel):
    app: AppConfig
    observer: ObserverConfig

def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Config:
    # Navigate to root project directory regardless of where script is run from
    root_dir = Path(__file__).resolve().parent.parent.parent
    config_path = root_dir / "config" / "default.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    return Box(config)
