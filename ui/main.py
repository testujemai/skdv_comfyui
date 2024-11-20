import gradio as gr

from extensions.skdv_comfyui.ui.generation_parameters import generation_parameters_ui
from extensions.skdv_comfyui.ui.workflow_importer import workflow_importer_ui
from extensions.skdv_comfyui.ui.character_parameters import character_parameters_ui
from extensions.skdv_comfyui.ui.extensions_chat_panel import comfyui_chat_panel_ui
from extensions.skdv_comfyui.ui.workflow_editor import workflow_editor_ui


def mount_ui():
    with gr.Tabs(elem_id="skdv_comfyui_tabs"):
        with gr.TabItem("Generation Settings"):
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        generation_parameters_ui()

                    with gr.Column():
                        workflow_importer_ui()

        with gr.TabItem("Character Settings"):
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        character_parameters_ui()

        with gr.TabItem("ComfyUI Chat Panel", visible=False):
            comfyui_chat_panel_ui()

        with gr.TabItem("Workflow Editor"):
            workflow_editor_ui()
