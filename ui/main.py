import gradio as gr


def mount_ui():
    with gr.Tabs(elem_id="skdv_comfyui_tabs"):
        with gr.TabItem("Generation Settings"):
            pass

        # with gr.TabItem("Workflow Editor"):
        #     pass
