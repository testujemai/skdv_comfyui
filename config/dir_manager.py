from pathlib import Path


class DirManager:
    __instance = None

    __EXT_DIR = Path("extensions/skdv_comfyui")
    __WEB_DIR = __EXT_DIR.joinpath("web")
    __WORKFLOW_DIR = __EXT_DIR.joinpath("workflows")
    __GENERATED_IMAGES_DIR = __EXT_DIR.joinpath("generated_images")
    __CONFIG_DIR = __EXT_DIR.joinpath("config")

    def __new__(cls) -> "DirManager":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __ensure_dir_exists(self, dir: Path):
        if dir.exists():
            return

        dir.mkdir()

    def __init__(self) -> None:
        self.__ensure_dir_exists(DirManager.__WORKFLOW_DIR)

    def get_web_dir(self):
        return DirManager.__WEB_DIR

    def get_workflows_dir(self):
        return DirManager.__WORKFLOW_DIR

    def get_images_dir(self):
        return DirManager.__GENERATED_IMAGES_DIR

    def get_config_dir(self):
        return DirManager.__CONFIG_DIR

    def __check_source_exists(self, source: Path, skip_check=False):
        if not source.exists() and not skip_check:
            raise FileNotFoundError(f"Path to {source} not found in extension.")

        return source.exists()

    def __get_from_module(self, module: Path, resource: str):
        self.__check_source_exists(module.joinpath(resource))
        return module.joinpath(resource)

    def __write_to_file(self, file_path: Path, content: str):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def get_or_create(self, file_path: Path):
        if not file_path.is_file():
            raise Exception(f"Path '{file_path}' is a directory")

        if file_path.exists():
            return

        file_path.touch()
        return file_path

    def test_path_from_web(self, file_name: str):
        return self.__check_source_exists(
            DirManager.__WEB_DIR.joinpath(file_name), skip_check=True
        )

    def get_from_web(self, file_name: str):
        return self.__get_from_module(DirManager.__WEB_DIR, file_name)

    def test_path_from_config(self, file_name: str):
        return self.__check_source_exists(
            DirManager.__CONFIG_DIR.joinpath(file_name), skip_check=True
        )

    def get_from_config(self, file_name: str):
        return self.__get_from_module(DirManager.__CONFIG_DIR, file_name)

    def save_to_config(self, file_path: Path, content: str):
        self.__write_to_file(file_path, content)
        return file_path

    def get_from_workflows(self, workflow_file: str):
        return self.__get_from_module(
            DirManager.__WORKFLOW_DIR, f"{workflow_file}.json"
        )

    def load_local_workflows(self):
        return list(self.get_workflows_dir().iterdir())

    def save_to_workflows(self, workflow_file_name: str, content: str):
        self.__write_to_file(
            DirManager.__WORKFLOW_DIR.joinpath(workflow_file_name), content
        )
        return DirManager.__WORKFLOW_DIR.joinpath(workflow_file_name)
