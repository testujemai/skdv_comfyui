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


def history_is_blank(history: dict):
    return len(history["visible"]) == 0 or len(history["internal"]) == 0


def remove_image_from_text(text: str):
    return text[: text.index("<img")] + text[text.index("skdv_comfyui/>'/>") + 17 :]


def remove_alt_text_from_internal(text: str):
    return text[: text.index("<comfyui")] + text[text.index("skdv_comfyui/>") + 14 :]


def text_contains_comfyui_image(text: str):
    return text.index("skdv_comfyui/>'/>") >= 0


def internal_text_contains_comfyui_image(text: str):
    return text.index("<comfyui") >= 0


def generate_image(character: str):
    global latest_image_tag, alt_image_text

    latest_image_tag = None
    alt_image_text = None

    workflow = ComfyWorkflow(CONFIG_HANDLER.current_workflow_file)
    workflow.set_positive_prompt("1girl, glasses")
    workflow.set_negative_prompt("bad quality")
    workflow.set_character(character)

    image_path, seed = ComfyAPI.generate(workflow)

    alt_image_text = f"<comfyui image, seed: {seed} - skdv_comfyui/>"
    latest_image_tag = f"<img src='file/{image_path.as_posix()}' style='max-width: unset;' alt='{alt_image_text}'/>\n"
    return gr.update(value=seed)


def send_image_message(image_tag: str | None, state: dict):
    history = state["history"]

    if image_tag is None:
        return history

    if latest_image_tag is None or alt_image_text is None:
        return history

    if history_is_blank(history):
        state["history"] = m_chat.load_latest_history(state)
        history = state["history"]

    history["visible"][-1][1] += image_tag
    history["internal"][-1][1] += apply_extensions(
        "input", alt_image_text, state, is_chat=True
    )
    return history


def remove_image_from_last_message(state: dict):
    history = state["history"]

    if history_is_blank(history):
        return history

    if internal_text_contains_comfyui_image(history["internal"][-1][1]):
        history["internal"][-1][1] = remove_alt_text_from_internal(
            history["internal"][-1][1]
        )

    if text_contains_comfyui_image(history["visible"][-1][1]):
        history["visible"][-1][1] = remove_image_from_text(history["visible"][-1][1])

    return history


def handle_remove_latest_image(chat_id: str, chat_html: str, state: dict):
    history = state["history"]
    html = chat_html

    if chat_id is not None:
        history = remove_image_from_last_message(state)
        m_chat.save_history(history, chat_id, state["character_menu"], state["mode"])

        html = m_chat.redraw_html(
            history,
            state["name1"],
            state["name2"],
            state["mode"],
            state["chat_style"],
            state["character_menu"],
        )

    return [history, html]


def handle_send_image_message_click(
    text: str, chat_id: str, chat_html: str, state: dict
):
    history = state["history"]
    html = chat_html

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


def comfyui_chat_panel_ui():
    with gr.Accordion("ComfyUI Generation", elem_id="skdv_comfyui_generation_panel"):
        pass

    hover_menu_generate_button = gr.Button(
        "Generate image: last message", elem_id="skdv_comfyui_button_generate"
    )

    hover_menu_regenerate_button = gr.Button(
        "Re-generate last image", elem_id="skdv_comfyui_button_regenerate"
    )

    hover_menu_remove_image_button = gr.Button(
        "Remove last image", elem_id="skdv_comfyui_button_remove_image"
    )

    hover_menu_generate_button.click(
        fn=generate_image,
        inputs=shared.gradio["character_menu"],
        outputs=shared_ui["previous-seed-display"],
        show_progress="full",
    ).then(
        fn=lambda: (latest_image_tag),
        outputs=m_utils.gradio("Chat input"),
    ).then(
        fn=handle_send_image_message_click,
        inputs=m_utils.gradio("Chat input", "unique_id", "display", "interface_state"),
        outputs=m_utils.gradio("history", "display", "Chat input"),
    )

    hover_menu_remove_image_button.click(
        fn=handle_remove_latest_image,
        inputs=m_utils.gradio("unique_id", "display", "interface_state"),
        outputs=m_utils.gradio("history", "display"),
    )

    hover_menu_regenerate_button.click(
        fn=handle_remove_latest_image,
        inputs=m_utils.gradio("unique_id", "display", "interface_state"),
        outputs=m_utils.gradio("history", "display"),
    ).then(
        fn=generate_image,
        inputs=shared.gradio["character_menu"],
        outputs=shared_ui["previous-seed-display"],
        show_progress="full",
    ).then(
        fn=lambda: (latest_image_tag),
        outputs=m_utils.gradio("Chat input"),
    ).then(
        fn=handle_send_image_message_click,
        inputs=m_utils.gradio("Chat input", "unique_id", "display", "interface_state"),
        outputs=m_utils.gradio("history", "display", "Chat input"),
    )
