import os
from typing import Optional

from dotenv import load_dotenv

from alvin_cli.config.loader import load_cfg_file
from alvin_cli.schemas.models import CamelBaseModel


class Settings(CamelBaseModel):
    alvin_api_host: str
    alvin_dbt_api_url: Optional[str] = "https://dbt.alvin.ai"
    alvin_api_token: str
    alvin_verbose_log: Optional[bool] = False

    def __init__(self) -> None:

        cfg_file = load_cfg_file()

        if not cfg_file:
            load_dotenv(f"{os.getcwd()}/.env")
            kwargs = {
                "alvin_api_host": os.getenv("ALVIN_API_HOST")
                if "ALVIN_API_HOST" in os.environ
                else "https://app.alvin.ai",
                "alvin_api_token": os.getenv("ALVIN_API_TOKEN")
                if "ALVIN_API_TOKEN" in os.environ
                else "",
                "alvin_verbose_log": os.getenv("ALVIN_VERBOSE_LOG")
                if "ALVIN_VERBOSE_LOG" in os.environ
                else False,
                "alvin_dbt_api_url": os.environ.get(
                    "ALVIN_DBT_API_URL", "https://dbt.alvin.ai",
                ),
            }
        else:
            kwargs = cfg_file
        super().__init__(**kwargs)
