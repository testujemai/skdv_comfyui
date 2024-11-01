import extensions.skdv_comfyui.ui.main as comfyui

params = {
    "display_name": "ComfyUI Panel",
    "is_tab": True,
}


def custom_css():
    return ""


def custom_js():
    return ""


def ui():
    comfyui.mount_ui()
