from pathlib import Path
from extensions.skdv_comfyui.config.config_handler import ConfigHandler
from extensions.skdv_comfyui.config.dir_manager import DirManager


DIR_MANAGER = DirManager()
CONFIG_HANDLER = ConfigHandler.setup()


class ComfyWorkflow:
    def __load_workflow(self, file: str) -> str:
        with open(DIR_MANAGER.get_from_workflows(file), "r") as workflow:
            return workflow.read()

    def __init__(self, workflow_file: str):
        self._raw_workflow = self.__load_workflow(workflow_file)
        self._positive_prompt = ""
        self._negative_prompt = ""

    def __avatar_to_base64(self, image_path: Path):
        # TODO: load image from path and convert to base64
        return ""

    def __parse_seed(self, seed: int):
        if seed >= 0:
            return seed

        # TODO: randomize seed
        return seed

    def inject_parameters(self) -> str:
        injected = f"{self._raw_workflow}"
        injected.replace(
            "%prompt%", CONFIG_HANDLER.shared_positive_prompt + self._positive_prompt
        )
        injected.replace(
            "%negative_prompt%",
            CONFIG_HANDLER.shared_negative_prompt + self._negative_prompt,
        )
        injected.replace("%model%", CONFIG_HANDLER.model)
        injected.replace("%vae%", CONFIG_HANDLER.vae)
        injected.replace("%sampler%", CONFIG_HANDLER.sampler)
        injected.replace("%scheduler%", CONFIG_HANDLER.scheduler)
        injected.replace("%steps%", str(CONFIG_HANDLER.steps))
        injected.replace("%scale%", str(CONFIG_HANDLER.cfg_scale))
        injected.replace("%clip_skip%", str(CONFIG_HANDLER.clip_skip))
        injected.replace("%width%", str(CONFIG_HANDLER.width))
        injected.replace("%height%", str(CONFIG_HANDLER.height))
        injected.replace("%user_avatar%", self.__avatar_to_base64(Path("/")))
        injected.replace("%char_avatar%", self.__avatar_to_base64(Path("/")))
        injected.replace("%seed%", str(self.__parse_seed(CONFIG_HANDLER.seed)))

        return injected
