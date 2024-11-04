import gradio as gr

from modules import shared

from extensions.skdv_comfyui.comfyui.api import ComfyAPI
from extensions.skdv_comfyui.comfyui.workflow import ComfyWorkflow
from extensions.skdv_comfyui.config.config_handler import ConfigHandler
from extensions.skdv_comfyui.ui.shared import shared_ui

CONFIG_HANDLER = ConfigHandler.setup()


def generate_image(character: str):
    workflow = ComfyWorkflow(CONFIG_HANDLER.current_workflow_file)
    workflow.set_positive_prompt("1girl, blonde")
    workflow.set_negative_prompt("glasses")
    workflow.set_character(character)

    shared.processing_message = "Generating Image..."
    image_path, seed = ComfyAPI.generate(workflow)

    return gr.update(value=seed)


def comfyui_chat_panel_ui():
    with gr.Accordion("ComfyUI Generation", elem_id="skdv_comfyui_generation_panel"):
        pass

    hover_menu_generate_button = gr.Button(
        "Generate image from last message", elem_id="skdv_comfyui_generate_button"
    )
    hover_menu_generate_button.click(
        generate_image,
        inputs=shared.gradio["character_menu"],
        outputs=shared_ui["previous-seed-display"],
    )
