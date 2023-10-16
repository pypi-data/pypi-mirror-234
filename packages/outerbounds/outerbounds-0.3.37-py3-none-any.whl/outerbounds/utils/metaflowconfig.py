import json
import os


def init_config():
    # Read configuration from $METAFLOW_HOME/config_<profile>.json.
    home = os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")
    profile = os.environ.get("METAFLOW_PROFILE")
    path_to_config = os.path.join(home, "config.json")
    if profile:
        path_to_config = os.path.join(home, "config_%s.json" % profile)
    path_to_config = os.path.expanduser(path_to_config)
    config = {}
    if os.path.exists(path_to_config):
        with open(path_to_config, encoding="utf-8") as f:
            return json.load(f)
    elif profile:
        raise Exception(
            "Unable to locate METAFLOW_PROFILE '%s' in '%s')" % (profile, home)
        )
    return config


def get_metaflow_token_from_config(config_dir: str, profile: str) -> str:
    """
    Return the Metaflow service auth key from the config file.

    Args:
        config_dir (str): Path to the config directory
        profile (str): The named metaflow profile
    """
    config_filename = f"config_{profile}.json" if profile else "config.json"
    config_path = os.path.join(config_dir, config_filename)
    with open(config_path) as json_file:
        config = json.load(json_file)
        if config is None or "METAFLOW_SERVICE_AUTH_KEY" not in config:
            raise Exception("METAFLOW_SERVICE_AUTH_KEY not found in config file")
        return config["METAFLOW_SERVICE_AUTH_KEY"]


def get_sanitized_url_from_config(config_dir: str, profile: str, key: str) -> str:
    """
    Given a key, return the value from the config file, with https:// prepended if not already present.

    Args:
        config_dir (str): Path to the config directory
        profile (str): The named metaflow profile
        key (str): The key to look up in the config file
    """
    config_filename = f"config_{profile}.json" if profile else "config.json"
    config_path = os.path.join(config_dir, config_filename)

    with open(config_path) as json_file:
        config = json.load(json_file)
        if key not in config:
            raise Exception(f"Key {key} not found in config file {config_path}")
        url_in_config = config[key]
        if not url_in_config.startswith("https://"):
            url_in_config = f"https://{url_in_config}"

        url_in_config = url_in_config.rstrip("/")
        return url_in_config
