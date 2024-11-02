import extensions.skdv_comfyui.ui.main as comfyui

from pathlib import Path

params = {
    "display_name": "ComfyUI Panel",
    "is_tab": True,
}


def load_skdv_comfyui_resource(path: str):
    with Path(f"extensions/skdv_comfyui{path}").open("r", encoding="utf-8") as f:
        f = f.read()

    return f


def custom_css():
    return load_skdv_comfyui_resource("/web/skdv_comfyui_styles.css")


def custom_js():
    return ""


def ui():
    comfyui.mount_ui()
