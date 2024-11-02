import gradio as gr

from extensions.skdv_comfyui.ui.generation_parameters import generation_parameters_ui
from extensions.skdv_comfyui.ui.workflow_importer import workflow_importer_ui


def mount_ui():
    with gr.Tabs(elem_id="skdv_comfyui_tabs"):
        with gr.TabItem("Generation Settings"):
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        generation_parameters_ui()

                    with gr.Column():
                        workflow_importer_ui()

        # with gr.TabItem("Workflow Editor"):
        #     pass
