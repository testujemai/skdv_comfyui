import extensions.skdv_comfyui.ui.main as comfyui
from extensions.skdv_comfyui.config.dir_manager import DirManager

params = {
    "display_name": "ComfyUI Panel",
    "is_tab": True,
}

dir_manager = DirManager()


def load_skdv_comfyui_resource(file: str):
    with dir_manager.get_from_web(file).open("r", encoding="utf-8") as f:
        f = f.read()

    return f


def custom_css():
    return load_skdv_comfyui_resource("skdv_comfyui_styles.css")


def custom_js():
    return load_skdv_comfyui_resource("skdv_autoconnect.js")


def ui():
    comfyui.mount_ui()
