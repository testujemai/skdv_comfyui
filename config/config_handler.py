__version__ = "0.0.0"
"""
This extensions version.
"""


class ConfigHandler:
    __instance = None

    def __init__(self, json_data: dict):
        self._api_url = json_data["api_url"]

    @staticmethod
    def setup():
        if ConfigHandler.__instance is not None:
            return ConfigHandler.__instance

        if "path to config exists" == "True":
            # load config and init with config
            return ConfigHandler.__instance

        ConfigHandler.__instance = ConfigHandler({"api_url": "http://127.0.0.1:8188"})
        return ConfigHandler.__instance
