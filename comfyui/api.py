import requests

from extensions.skdv_comfyui.config.config_handler import ConfigHandler
from extensions.skdv_comfyui.config.dir_manager import DirManager

CONFIG_HANDLER = ConfigHandler.setup()
DIR_MANAGER = DirManager()


class ComfyAPI:
    @staticmethod
    def ping():
        try:
            requests.get(CONFIG_HANDLER.api_url + "/system_stats")
            return True
        except Exception as e:
            print(f"Could not connect to ComfyUI:\n{e}")
            return False

    @staticmethod
    def get_generation_info() -> dict:
        try:
            return requests.get(CONFIG_HANDLER.api_url + "/object_info").json()
        except Exception as e:
            print(f"Could not fetch generation parameters:\n{e}")
            return {}

    @staticmethod
    def get_samplers(generation_info: dict | None = None) -> list[str]:
        response = generation_info or ComfyAPI.get_generation_info()
        return response["KSampler"]["input"]["required"]["sampler_name"][0]

    @staticmethod
    def get_models(generation_info: dict | None = None) -> list[str]:
        response = generation_info or ComfyAPI.get_generation_info()
        return response["CheckpointLoaderSimple"]["input"]["required"]["ckpt_name"][0]

    @staticmethod
    def get_schedulers(generation_info: dict | None = None) -> list[str]:
        response = generation_info or ComfyAPI.get_generation_info()
        return response["KSampler"]["input"]["required"]["scheduler"][0]

    @staticmethod
    def get_vaes(generation_info: dict | None = None) -> list[str]:
        response = generation_info or ComfyAPI.get_generation_info()
        return response["VAELoader"]["input"]["required"]["vae_name"][0]
