import gradio as gr

import modules.chat as m_chat
import modules.utils as m_utils
from modules.extensions import apply_extensions
from modules import shared

from extensions.skdv_comfyui.comfyui.api import ComfyAPI
from extensions.skdv_comfyui.comfyui.workflow import ComfyWorkflow
from extensions.skdv_comfyui.config.config_handler import ConfigHandler
from extensions.skdv_comfyui.ui.shared import shared_ui

CONFIG_HANDLER = ConfigHandler.setup()

latest_image_tag = None
alt_image_text = None


def send_image_message(image_tag: str, state: dict):
    history = state["history"]

    if latest_image_tag is None or alt_image_text is None:
        return history

    if len(history["visible"]) == 0:
        history["visible"].append(["", ""])
        history["internal"].append(["", ""])

    history = state["history"]
    history["visible"][-1][1] += image_tag
    history["internal"][-1][1] += apply_extensions(
        "input", alt_image_text, state, is_chat=True
    )
    return history


def handle_send_image_message_click(text: str, chat_id: str, state: dict):
    history = state["history"]
    if latest_image_tag is not None and alt_image_text is not None:
        history = send_image_message(text, state)
        m_chat.save_history(history, chat_id, state["character_menu"], state["mode"])

    html = m_chat.redraw_html(
        history,
        state["name1"],
        state["name2"],
        state["mode"],
        state["chat_style"],
        state["character_menu"],
    )

    return [history, html, ""]


def generate_image(character: str):
    global latest_image_tag, alt_image_text
    latest_image_tag = None
    alt_image_text = None

    workflow = ComfyWorkflow(CONFIG_HANDLER.current_workflow_file)
    workflow.set_positive_prompt("1girl, glasses")
    workflow.set_negative_prompt("bad quality")
    workflow.set_character(character)

    shared.processing_message = "Generating Image..."
    image_path, seed = ComfyAPI.generate(workflow)

    alt_image_text = f"ComfyUI image, seed: {seed}"
    latest_image_tag = f"<img src='file/{image_path.as_posix()}' alt='{alt_image_text}' style='max-width: unset;'/>\n"
    return gr.update(value=seed)


def comfyui_chat_panel_ui():
    with gr.Accordion("ComfyUI Generation", elem_id="skdv_comfyui_generation_panel"):
        pass

    hover_menu_generate_button = gr.Button(
        "Generate image: last message", elem_id="skdv_comfyui_generate_button"
    )
    hover_menu_generate_button.click(
        fn=generate_image,
        inputs=shared.gradio["character_menu"],
        outputs=shared_ui["previous-seed-display"],
        show_progress="full",
    ).then(
        fn=lambda: (latest_image_tag),
        outputs=m_utils.gradio("Chat input"),
        show_progress="hidden",
    ).then(
        fn=handle_send_image_message_click,
        inputs=m_utils.gradio("Chat input", "unique_id", "interface_state"),
        outputs=m_utils.gradio("history", "display", "Chat input"),
        show_progress="hidden",
    )
