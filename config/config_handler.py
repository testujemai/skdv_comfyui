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
    "shared_positive_prompt": "",
    "shared_negative_prompt": "",
    "edit_before_generating": False,
    "interactive_mode": False,
    "unload_text_model_before_generating": False,
}

dir_manager = DirManager()


class CharacterPrompt:
    def __init__(self, character: str, positive: str, negative: str):
        self._character = character
        self._positive = positive
        self._negative = negative

    @property
    def positive(self):
        return self._positive

    @property
    def negative(self):
        return self._negative

    @property
    def character(self):
        return self._character

    def __eq__(self, value: object, /) -> bool:
        if type(value) is not type(self):
            return False

        return self._character == value.character


class ConfigHandler:
    __instance: "ConfigHandler | None" = None
    __loaded_config: dict | None = None
    __loaded_character_prompts: dict[str, str] | None = None

    def __new__(cls) -> "ConfigHandler":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __config_load_or_defaults(self, key: str):
        if ConfigHandler.__loaded_config is None:
            return DEFAULT_CONFIG[key]

        if key not in ConfigHandler.__loaded_config.keys():
            return DEFAULT_CONFIG[key]

        return ConfigHandler.__loaded_config[key]

    def __init__(self):
        if ConfigHandler.__loaded_config is None:
            raise Exception(
                "Attempted to load an empty configuration. Was .setup() called?"
            )

        self._api_url: str = self.__config_load_or_defaults("api_url")
        self._current_workflow_file: str = self.__config_load_or_defaults(
            "current_workflow_file"
        )
        self._model: str = self.__config_load_or_defaults("model")
        self._vae: str = self.__config_load_or_defaults("vae")
        self._width: int = self.__config_load_or_defaults("width")
        self._height: int = self.__config_load_or_defaults("height")
        self._sampler: str = self.__config_load_or_defaults("sampler")
        self._scheduler: str = self.__config_load_or_defaults("scheduler")
        self._steps: int = self.__config_load_or_defaults("steps")
        self._cfg_scale: float = self.__config_load_or_defaults("cfg_scale")
        self._clip_skip: int = self.__config_load_or_defaults("clip_skip")
        self._seed: int = self.__config_load_or_defaults("seed")
        self._shared_positive_prompt: str = self.__config_load_or_defaults(
            "shared_positive_prompt"
        )
        self._shared_negative_prompt: str = self.__config_load_or_defaults(
            "shared_negative_prompt"
        )
        self._unload_text_model_before_generating: bool = (
            self.__config_load_or_defaults("unload_text_model_before_generating")
        )

        self._character_prompts: list[CharacterPrompt] = []
        if ConfigHandler.__loaded_character_prompts is not None:
            for chara, prompts in ConfigHandler.__loaded_character_prompts.items():
                self._character_prompts.append(
                    CharacterPrompt(chara, prompts[0], prompts[1])
                )

    @staticmethod
    def setup():
        if ConfigHandler.__instance is not None:
            return ConfigHandler.__instance

        if dir_manager.test_path_from_config("config.json"):
            with open(dir_manager.get_from_config("config.json"), "r") as config:
                ConfigHandler.__loaded_config = json.loads(config.read())

        if dir_manager.test_path_from_config("character_prompts.json"):
            with open(
                dir_manager.get_from_config("character_prompts.json"), "r"
            ) as prompts:
                ConfigHandler.__loaded_character_prompts = json.loads(prompts.read())

        if ConfigHandler.__loaded_config is not None:
            return ConfigHandler()

        ConfigHandler.__loaded_config = DEFAULT_CONFIG
        ConfigHandler.__loaded_character_prompts = {}
        instance = ConfigHandler()
        instance.save()
        return instance

    def save(self):
        print("saving")
        config_file_path = dir_manager.get_or_create(
            dir_manager.create_path_from_config("config.json")
        )
        dir_manager.save_to_config(config_file_path, json.dumps(self.to_dict()))

        characters_file_path = dir_manager.get_or_create(
            dir_manager.create_path_from_config("character_prompts.json")
        )
        dir_manager.save_to_config(
            characters_file_path,
            json.dumps(
                {c.character: [c.positive, c.negative] for c in self._character_prompts}
            ),
        )

    @property
    def api_url(self):
        return self._api_url

    def set_api_url(self, new_url: str):
        self._api_url = new_url
        self.save()

    @property
    def current_workflow_file(self):
        return self._current_workflow_file

    def set_current_workflow_file(self, file_name: str):
        self._current_workflow_file = file_name
        self.save()

    @property
    def model(self):
        return self._model

    def set_model(self, new_model: str):
        self._model = new_model
        self.save()

    @property
    def vae(self):
        return self._vae

    def set_vae(self, new_vae: str):
        self._vae = new_vae
        self.save()

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

    def set_sampler(self, new_sampler: str):
        self._sampler = new_sampler
        self.save()

    @property
    def scheduler(self):
        return self._scheduler

    def set_scheduler(self, new_scheduler: str):
        self._scheduler = new_scheduler
        self.save()

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

    @property
    def shared_positive_prompt(self):
        return self._shared_positive_prompt

    def set_shared_positive_prompt(self, prompt: str):
        self._shared_positive_prompt = prompt
        self.save()

    @property
    def shared_negative_prompt(self):
        return self._shared_negative_prompt

    def set_shared_negative_prompt(self, prompt: str):
        self._shared_negative_prompt = prompt
        self.save()

    @property
    def unload_text_model_before_generating(self):
        return self._unload_text_model_before_generating

    def set_unload_text_model_before_generating(self, unload: bool):
        self._unload_text_model_before_generating = unload
        self.save()

    def get_character_prompts(self, character: str) -> CharacterPrompt | None:
        if character not in [chara.character for chara in self._character_prompts]:
            return None

        for chara in self._character_prompts:
            if chara.character == character:
                return chara

        raise ValueError(f"CharacterPrompt not found for: {character}")

    def save_character_prompt(self, character_prompts: CharacterPrompt):
        # delete previous if any
        for index, chara in enumerate(self._character_prompts):
            if chara == character_prompts:
                del self._character_prompts[index]

        self._character_prompts.append(character_prompts)
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
            "shared_positive_prompt": self._shared_positive_prompt,
            "shared_negative_prompt": self._shared_positive_prompt,
            "unload_text_model_before_generating": self._unload_text_model_before_generating,
        }
