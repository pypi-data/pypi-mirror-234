# ruff: noqa: BLE001
import configparser
import os
import traceback
from os.path import expanduser
from typing import Dict, Optional

CFG_CREDENTIALS_DICT = {
    "ALVIN_API_TOKEN": "your_newly_generated_token",
    "ALVIN_API_HOST": "https://app.alvin.ai",
    "ALVIN_DBT_API_URL": "https://dbt.alvin.ai",
    "ALVIN_VERBOSE_LOG": "false",
}
USER_CONFIG_DIR = expanduser("~") + "/.alvin"
USER_CONFIG = USER_CONFIG_DIR + "/alvin.cfg"
CONFIG = configparser.ConfigParser()
GLOBAL = "GLOBAL"
CORE_SECTION = "ALVIN"


def create_cfg_file(directory_path: str) -> bool:
    config_write = configparser.ConfigParser()
    config_write.add_section(CORE_SECTION)
    config_write.add_section(GLOBAL)
    config_write[GLOBAL]["active_profile"] = CORE_SECTION

    for k, v in CFG_CREDENTIALS_DICT.items():
        config_write[CORE_SECTION][k] = v

    alvin_cfg_file_path = directory_path + "/alvin.cfg"

    if os.path.isfile(alvin_cfg_file_path):
        return True

    with open(alvin_cfg_file_path, "w") as f:
        config_write.write(f)
    return False


def current_active_project_name(config_read: configparser.ConfigParser) -> str:
    """Is active project set up? Return name if yes else None"""
    return config_read[GLOBAL]["active_profile"]


def set_current_config_context(context: str) -> bool:
    """Set up the context in active project"""
    CONFIG.read(USER_CONFIG)
    if context in CONFIG.sections():
        CONFIG.set(GLOBAL, "active_profile", context)
        with open(USER_CONFIG, "w+") as f:
            CONFIG.write(f)
        return True

    return False


def set_key_value_in_cfg(current_section: str, key: str, value: str) -> Optional[bool]:
    """Update this function to write particular sections to the cfg file"""
    try:
        config = configparser.ConfigParser()
        config.read(USER_CONFIG)

        if os.path.isfile(USER_CONFIG):
            current_section = current_section.upper()
            if current_section not in config.sections():
                config.add_section(section=current_section)
            config.set(current_section, key, value)
            with open(USER_CONFIG, "w+") as f:
                config.write(f)
        return True

    except Exception:
        return False


def load_cfg_file() -> Dict:
    """Load credentials from cfg file"""
    config_read = configparser.ConfigParser()

    if not os.path.isfile(USER_CONFIG):
        return {}

    config_read.read(USER_CONFIG)

    try:
        if config_read:
            credentials = {}
            for k, _ in CFG_CREDENTIALS_DICT.items():
                credentials.update({k.lower(): config_read[CORE_SECTION].get(k)})

            if credentials.get("alvin_dbt_api_url", None) is None:
                credentials.update({"alvin_dbt_api_url": "https://dbt.alvin.ai"})

            return credentials
    except Exception:
        print(f"Unable to load config file at: {USER_CONFIG}, try removing it")

        # this needs to use the env var since settings was not loaded properly.
        if os.getenv("ALVIN_VERBOSE_LOG"):
            traceback.print_exc()

    return {}
