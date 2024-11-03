import json

from extensions.skdv_comfyui.config.dir_manager import DirManager

__version__ = "0.0.0"
"""
This extensions version.
"""

DEFAULT_CONFIG = {
    "api_url": "http://127.0.0.1:8188",
    "current_workflow_file": "",
    "model": "",
    "vae": "",
    "width": 512,
    "height": 512,
    "sampler": "",
    "scheduler": "",
    "steps": 20,
    "cfg_scale": 7,
    "clip_skip": 0,
    "seed": -1,
}

dir_manager = DirManager()


class ConfigHandler:
    __instance: "ConfigHandler | None" = None
    __loaded_config: dict | None = None

    def __new__(cls) -> "ConfigHandler":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self):
        if ConfigHandler.__loaded_config is None:
            raise Exception("Attempted to load an empty configuration.")

        self._api_url = ConfigHandler.__loaded_config["api_url"]
        self._current_workflow_file = ConfigHandler.__loaded_config[
            "current_workflow_file"
        ]
        self._model = ConfigHandler.__loaded_config["model"]
        self._vae = ConfigHandler.__loaded_config["vae"]
        self._width = ConfigHandler.__loaded_config["width"]
        self._height = ConfigHandler.__loaded_config["height"]
        self._sampler = ConfigHandler.__loaded_config["sampler"]
        self._scheduler = ConfigHandler.__loaded_config["scheduler"]
        self._steps = ConfigHandler.__loaded_config["steps"]
        self._cfg_scale = ConfigHandler.__loaded_config["cfg_scale"]
        self._clip_skip = ConfigHandler.__loaded_config["clip_skip"]
        self._seed = ConfigHandler.__loaded_config["seed"]

    @staticmethod
    def setup():
        if ConfigHandler.__instance is not None:
            return ConfigHandler.__instance

        ConfigHandler.__loaded_config = DEFAULT_CONFIG
        if dir_manager.test_path_from_config("config.json"):
            with open(dir_manager.get_from_config("config.json"), "r") as config:
                ConfigHandler.__loaded_config = json.loads(config.read())

        return ConfigHandler()

    def to_dict(self):
        return {
            "api_url": self._api_url,
            "current_workflow_file": self._current_workflow_file,
            "model": self._model,
            "vae": self._vae,
            "width": self._width,
            "height": self._height,
            "sampler": self._sampler,
            "scheduler": self._scheduler,
            "steps": self._steps,
            "cfg_scale": self._cfg_scale,
            "clip_skip": self._clip_skip,
            "seed": self._seed,
        }

    def save(self):
        dir_manager.save_to_config(
            dir_manager.get_from_config("config.json"), json.dumps(self.to_dict())
        )
