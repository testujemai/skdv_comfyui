import gradio as gr
import modules.ui as oobabooga_ui

from extensions.skdv_comfyui.config.config_handler import ConfigHandler
from extensions.skdv_comfyui.config.dir_manager import DirManager

dir_manager = DirManager()
config_handler = ConfigHandler.setup()

CONNECTED_COLOR = "#1eab10"
DISCONNECTED_COLOR = "#b71717"
CONNECTING_COLOR = "#dfdb0c"

has_connected = False


def load_local_workflows() -> list:
    return [file.name for file in dir_manager.load_local_workflows()]


def update_workflow_file(file_name: str):
    config_handler.set_current_workflow_file(file_name)
    gr.Info("Workflow Loaded")


def switch_to_random_seed():
    config_handler.set_seed(-1)
    return gr.update(value=-1)


def generation_parameters_ui():
    gr.Markdown("## Generation Parameters")

    with gr.Row():
        api_url_input = gr.Textbox(
            value=config_handler.api_url,
            max_lines=1,
            interactive=True,
            label="ComfyUI Endpoint",
            elem_classes=["slim-dropdown"],
            scale=3,
        )

        connect_button = gr.Button(
            "Connect", elem_classes=["skdv-button-height", "skdv-align-button-bottom"]
        )
        connection_status_label = gr.Label(
            "Disconnected",
            color=DISCONNECTED_COLOR,
            show_label=False,
            elem_classes=["skdv-connection-status", "skdv-align-button-bottom"],
        )

    with gr.Row():
        workflow_dropdown = gr.Dropdown(
            load_local_workflows(),
            value=config_handler.current_workflow_file,
            label="Select a ComfyUI workflow",
            interactive=True,
            elem_classes=["slim-dropdown"],
            scale=2,
        )
        load_workflow_button = gr.Button(
            "Load", elem_classes=["skdv-button-height", "skdv-align-button-bottom"]
        )

        oobabooga_ui.create_refresh_button(
            workflow_dropdown,
            lambda: None,
            lambda: {
                "choices": load_local_workflows(),
                "value": config_handler.current_workflow_file,
            },
            ["refresh-button"],
        )

        load_workflow_button.click(
            fn=lambda file: update_workflow_file(file), inputs=workflow_dropdown
        )

    with gr.Row():
        model_dropdown = gr.Dropdown(
            ["a.safetensors", "b.safetensors", "c.safetensors"], label="Model"
        )
        vae_dropdown = gr.Dropdown(["vae1", "vae2", "vae3"], label="VAE")

    with gr.Row():
        resolution_dropdown = gr.Dropdown(["832x1216"], label="Resolution Preset")

    with gr.Row():
        width_slider = gr.Slider(
            128,
            4096,
            value=config_handler.width,
            step=1,
            label="Width",
            interactive=True,
        )
        height_slider = gr.Slider(
            128,
            4096,
            value=config_handler.height,
            step=1,
            label="Height",
            interactive=True,
        )

        width_slider.release(
            fn=lambda width: config_handler.set_width(width), inputs=width_slider
        )
        height_slider.release(
            fn=lambda height: config_handler.set_height(height), inputs=height_slider
        )

    with gr.Row():
        sampler_dropdown = gr.Dropdown(["euler", "euler a"], label="Sampler")
        scheduler_dropdown = gr.Dropdown(["normal", "karras"], label="Scheduler")

    with gr.Row():
        sampler_steps_slider = gr.Slider(
            1, 150, value=config_handler.steps, label="Sampling Steps", interactive=True
        )
        cfg_scale_slider = gr.Slider(
            1,
            30,
            value=config_handler.cfg_scale,
            step=0.5,
            label="CFG Scale",
            interactive=True,
        )

        sampler_steps_slider.release(
            fn=lambda steps: config_handler.set_steps(steps),
            inputs=sampler_steps_slider,
        )
        cfg_scale_slider.release(
            fn=lambda cfg: config_handler.set_cfg_scale(cfg), inputs=cfg_scale_slider
        )

    with gr.Row():
        clip_skip_slider = gr.Slider(
            -12,
            12,
            value=config_handler.clip_skip,
            step=1,
            label="CLIP Skip",
            info="Use positive or negative CLIP skip depending on your workflow configuration.",
            interactive=True,
        )

        clip_skip_slider.release(
            fn=lambda clip_skip: config_handler.set_clip_skip(clip_skip),
            inputs=clip_skip_slider,
        )

    with gr.Row():
        with gr.Column():
            seed_input = gr.Number(
                value=config_handler.seed,
                step=1,
                label="Seed",
                interactive=True,
                info="Use -1 for a random seed.",
            )
            previous_seed_display = gr.Number(
                value=config_handler.seed,
                interactive=False,
                label="Last generated seed",
            )

        with gr.Column():
            random_seed_button = gr.Button(
                value="Random",
                size="lg",
                elem_classes=["skdv-full-height-btn"],
            )
            reuse_seed_button = gr.Button(
                value="Re-use last seed",
                size="lg",
                elem_classes=["skdv-full-height-btn"],
            )

            random_seed_button.click(fn=switch_to_random_seed, outputs=seed_input)
