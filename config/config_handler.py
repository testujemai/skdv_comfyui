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

        self._api_url: str = ConfigHandler.__loaded_config["api_url"]
        self._current_workflow_file: str = ConfigHandler.__loaded_config[
            "current_workflow_file"
        ]
        self._model: str = ConfigHandler.__loaded_config["model"]
        self._vae: str = ConfigHandler.__loaded_config["vae"]
        self._width: int = ConfigHandler.__loaded_config["width"]
        self._height: int = ConfigHandler.__loaded_config["height"]
        self._sampler: str = ConfigHandler.__loaded_config["sampler"]
        self._scheduler: str = ConfigHandler.__loaded_config["scheduler"]
        self._steps: int = ConfigHandler.__loaded_config["steps"]
        self._cfg_scale: float = ConfigHandler.__loaded_config["cfg_scale"]
        self._clip_skip: int = ConfigHandler.__loaded_config["clip_skip"]
        self._seed: int = ConfigHandler.__loaded_config["seed"]

    @staticmethod
    def setup():
        if ConfigHandler.__instance is not None:
            return ConfigHandler.__instance

        if dir_manager.test_path_from_config("config.json"):
            with open(dir_manager.get_from_config("config.json"), "r") as config:
                ConfigHandler.__loaded_config = json.loads(config.read())

            return ConfigHandler()

        ConfigHandler.__loaded_config = DEFAULT_CONFIG
        instance = ConfigHandler()
        instance.save()
        return instance

    def save(self):
        print("saving")
        config_file_path = dir_manager.get_or_create(
            dir_manager.create_path_from_config("config.json")
        )
        dir_manager.save_to_config(config_file_path, json.dumps(self.to_dict()))

    @property
    def api_url(self):
        return self._api_url

    @property
    def current_workflow_file(self):
        return self._current_workflow_file

    def set_current_workflow_file(self, file_name: str):
        self._current_workflow_file = file_name
        self.save()

    @property
    def model(self):
        return self._model

    @property
    def vae(self):
        return self._vae

    @property
    def width(self):
        return self._width

    def set_width(self, width: int):
        self._width = width
        self.save()

    @property
    def height(self):
        return self._height

    def set_height(self, height: int):
        self._height = height
        self.save()

    @property
    def sampler(self):
        return self._sampler

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def steps(self):
        return self._steps

    def set_steps(self, new_steps: int):
        self._steps = new_steps
        self.save()

    @property
    def cfg_scale(self):
        return self._cfg_scale

    def set_cfg_scale(self, new_cfg: float):
        self._cfg_scale = new_cfg
        self.save()

    @property
    def clip_skip(self):
        return self._clip_skip

    def set_clip_skip(self, new_clip_skip: int):
        self._clip_skip = new_clip_skip
        self.save()

    @property
    def seed(self):
        return self._seed

    def set_seed(self, new_seed: int):
        self._seed = new_seed
        self.save()

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
