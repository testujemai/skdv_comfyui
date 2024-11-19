from pathlib import Path
from typing import Literal
import gradio as gr

from extensions.skdv_comfyui.textgen.utils import give_VRAM_priority_to
import modules.chat as m_chat
import modules.utils as m_utils
from modules import shared

from extensions.skdv_comfyui.comfyui.api import ComfyAPI
from extensions.skdv_comfyui.comfyui.workflow import ComfyWorkflow
from extensions.skdv_comfyui.config.config_handler import CharacterPrompt, ConfigHandler
from extensions.skdv_comfyui.ui.shared import shared_ui

CONFIG_HANDLER = ConfigHandler.setup()

latest_image_tag = None
alt_image_text = None


def history_is_blank(history: dict):
    return len(history["visible"]) == 0 or len(history["internal"]) == 0


def ping_comfyui():
    if not ComfyAPI.ping():
        gr.Warning("Disconnected from ComfyUI")


def remove_image_from_text(text: str):
    return text[: text.index("<img")] + text[text.index("skdv_comfyui/>'/>") + 17 :]


def remove_alt_text_from_internal(text: str):
    return text[: text.index("<comfyui")] + text[text.index("skdv_comfyui/>") + 14 :]


def text_contains_comfyui_image(text: str):
    try:
        return text.index("skdv_comfyui/>'/>") >= 0
    except ValueError:
        return False


def internal_text_contains_comfyui_image(text: str):
    try:
        return text.index("<comfyui") >= 0
    except ValueError:
        return False


def create_image_tag(image_path: Path, alt_image_text: str):
    return f"<img src='file/{image_path.as_posix()}' class='skdv-generated-image' onclick='skdvExpandImage(this)' alt='{alt_image_text}'/>\n"


def get_character_prompt(
    prompt_type: Literal["positive"] | Literal["negative"],
    character_name: str | None = None,
):
    character = CONFIG_HANDLER.get_character_prompts(
        character_name or shared.gradio["name2"].value
    )
    if character is None:
        return None

    return character.positive if prompt_type == "positive" else character.negative


def save_character_prompt(prompt: str, is_positive: bool, state: dict):
    previous = CONFIG_HANDLER.get_character_prompts(state["name2"])
    if previous is None:
        inverse_prompt = ""
    else:
        inverse_prompt = previous.negative if is_positive else previous.positive

    if is_positive:
        character = CharacterPrompt(state["name2"], prompt, inverse_prompt)
    else:
        character = CharacterPrompt(state["name2"], inverse_prompt, prompt)

    CONFIG_HANDLER.save_character_prompt(character)


def generate_image(character: str, positive: str, negative: str):
    global latest_image_tag, alt_image_text
    ping_comfyui()
    if not ComfyAPI.ping():
        return gr.update()

    if CONFIG_HANDLER.unload_text_model_before_generating:
        give_VRAM_priority_to("imagegen")

    latest_image_tag = None
    alt_image_text = None

    workflow = ComfyWorkflow(CONFIG_HANDLER.current_workflow_file)
    workflow.set_positive_prompt(positive)
    workflow.set_negative_prompt(negative)
    workflow.set_character(character)

    image_path, seed = ComfyAPI.generate(workflow)

    alt_image_text = f"<comfyui image, seed: {seed} - skdv_comfyui/>"
    latest_image_tag = create_image_tag(image_path, alt_image_text)
    return gr.update(value=seed)


def send_image_message(
    image_tag: str | None, history: dict[str, list[list[str]]], state: dict
):
    new_history = history

    if image_tag is None:
        return history

    if latest_image_tag is None or alt_image_text is None:
        return history

    if history_is_blank(history):
        new_history = m_chat.load_latest_history(state)

    new_history["visible"][-1][1] += image_tag
    new_history["internal"][-1][1] += alt_image_text
    return new_history


def remove_image_from_last_message(history: dict[str, list[list[str]]]):
    new_history = history

    if history_is_blank(new_history):
        return new_history

    if internal_text_contains_comfyui_image(new_history["internal"][-1][1]):
        new_history["internal"][-1][1] = remove_alt_text_from_internal(
            new_history["internal"][-1][1]
        )

    if text_contains_comfyui_image(new_history["visible"][-1][1]):
        new_history["visible"][-1][1] = remove_image_from_text(
            new_history["visible"][-1][1]
        )

    return new_history


def handle_remove_latest_image(
    chat_id: str, chat_html: str, history: dict[str, list[list[str]]], state: dict
):
    new_history = history
    html = chat_html

    if chat_id is not None:
        new_history = remove_image_from_last_message(new_history)
        m_chat.save_history(
            new_history, chat_id, state["character_menu"], state["mode"]
        )

        html = m_chat.redraw_html(
            history,
            state["name1"],
            state["name2"],
            state["mode"],
            state["chat_style"],
            state["character_menu"],
        )

    return [new_history, html]


def handle_send_image_message_click(
    text: str,
    chat_id: str,
    chat_html: str,
    history: dict[str, list[list[str]]],
    state: dict,
):
    new_history = history
    html = chat_html

    if latest_image_tag is not None and alt_image_text is not None:
        new_history = send_image_message(text, new_history, state)
        m_chat.save_history(
            new_history, chat_id, state["character_menu"], state["mode"]
        )

        html = m_chat.redraw_html(
            history,
            state["name1"],
            state["name2"],
            state["mode"],
            state["chat_style"],
            state["character_menu"],
        )

    if CONFIG_HANDLER.unload_text_model_before_generating:
        give_VRAM_priority_to("textgen")

    return [new_history, html, ""]


def comfyui_chat_panel_ui():
    generation_dots = gr.HTML(
        value='<div class="typing skdv-typing-dots"><span></span><span class="dot1"></span><span class="dot2"></span></div>',
        label="typing",
        elem_id="skdv_comfyui_generating_dots",
        visible=False,
    )

    hover_menu_generate_button = gr.Button(
        "Generate image: last message", elem_id="skdv_comfyui_button_generate"
    )

    hover_menu_regenerate_button = gr.Button(
        "Re-generate last image", elem_id="skdv_comfyui_button_regenerate"
    )

    hover_menu_remove_image_button = gr.Button(
        "Remove last image", elem_id="skdv_comfyui_button_remove_image"
    )

    with gr.Accordion(
        "ComfyUI Generation Parameters",
        open=False,
        elem_id="skdv_comfyui_generation_panel",
    ):
        unload_text_model_checkbox = gr.Checkbox(
            value=CONFIG_HANDLER.unload_text_model_before_generating,
            label="Unload text model before generating image",
            interactive=True,
        )

        character_selected = gr.Markdown(
            value="### Editing prompts for: *None*",
        )
        character_positive_prompt_input = gr.TextArea(
            value=get_character_prompt("positive"),
            placeholder="glasses, uniform, ...",
            interactive=True,
            label="Positive Prompt",
            lines=3,
        )
        character_negative_prompt_input = gr.TextArea(
            value=get_character_prompt("negative"),
            placeholder="black hair, jeans, ...",
            interactive=True,
            label="Negative Prompt",
            lines=3,
        )

        unload_text_model_checkbox.input(
            fn=lambda checked: CONFIG_HANDLER.set_unload_text_model_before_generating(
                checked
            ),
            inputs=unload_text_model_checkbox,
        )

        shared.gradio["name2"].change(
            fn=lambda name: gr.update(value=f"### Editing prompts for: *{name}*"),
            inputs=shared.gradio["character_menu"],
            outputs=character_selected,
        ).then(
            fn=lambda chara: (
                get_character_prompt("positive", chara),
                get_character_prompt("negative", chara),
            ),
            inputs=shared.gradio["character_menu"],
            outputs=[character_positive_prompt_input, character_negative_prompt_input],
        )

        character_positive_prompt_input.input(
            fn=lambda prompt, state: save_character_prompt(prompt, True, state),
            inputs=[character_positive_prompt_input]
            + m_utils.gradio("interface_state"),
        )
        character_negative_prompt_input.input(
            fn=lambda prompt, state: save_character_prompt(prompt, False, state),
            inputs=[character_negative_prompt_input]
            + m_utils.gradio("interface_state"),
        )

    hover_menu_generate_button.click(
        lambda: gr.update(visible=True), outputs=generation_dots, show_progress="hidden"
    ).then(
        fn=generate_image,
        inputs=[
            shared.gradio["character_menu"],
            character_positive_prompt_input,
            character_negative_prompt_input,
        ],
        outputs=shared_ui["previous-seed-display"],
        show_progress="hidden",
    ).then(
        fn=lambda: (latest_image_tag),
        outputs=m_utils.gradio("Chat input"),
        show_progress="hidden",
    ).then(
        fn=handle_send_image_message_click,
        inputs=m_utils.gradio(
            "Chat input", "unique_id", "display", "history", "interface_state"
        ),
        outputs=m_utils.gradio("history", "display", "Chat input"),
        show_progress="hidden",
    ).then(
        fn=lambda: gr.update(visible=False),
        outputs=generation_dots,
        show_progress="hidden",
    )

    hover_menu_remove_image_button.click(
        fn=handle_remove_latest_image,
        inputs=m_utils.gradio("unique_id", "display", "history", "interface_state"),
        outputs=m_utils.gradio("history", "display"),
        show_progress="hidden",
    )

    hover_menu_regenerate_button.click(
        lambda: gr.update(visible=True), outputs=generation_dots, show_progress="hidden"
    ).then(
        fn=handle_remove_latest_image,
        inputs=m_utils.gradio("unique_id", "display", "history", "interface_state"),
        outputs=m_utils.gradio("history", "display"),
        show_progress="hidden",
    ).then(
        fn=generate_image,
        inputs=[
            shared.gradio["character_menu"],
            character_positive_prompt_input,
            character_negative_prompt_input,
        ],
        outputs=shared_ui["previous-seed-display"],
        show_progress="hidden",
    ).then(
        fn=lambda: (latest_image_tag),
        outputs=m_utils.gradio("Chat input"),
        show_progress="hidden",
    ).then(
        fn=handle_send_image_message_click,
        inputs=m_utils.gradio(
            "Chat input", "unique_id", "display", "history", "interface_state"
        ),
        outputs=m_utils.gradio("history", "display", "Chat input"),
        show_progress="hidden",
    ).then(
        fn=lambda: gr.update(visible=False),
        outputs=generation_dots,
        show_progress="hidden",
    )
