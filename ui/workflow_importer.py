import gradio as gr
import json
import os

from gradio.utils import NamedString


def parse_json_file(file_path: NamedString) -> dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON file."}


def on_workflow_upload(file_path: NamedString | None):
    if file_path is None:
        return gr.update(value={}), gr.update(visible=False)

    parsed_json = parse_json_file(file_path)
    return gr.update(value=parsed_json), gr.update(
        visible=not bool("error" in parsed_json.keys())
    )


def on_workflow_import(file_path: NamedString | None):
    if file_path is None:
        return gr.update(value={}), gr.update(visible=False)

    parsed_json = parse_json_file(file_path)
    # TODO: make sure 'workflows' folder exists
    # write parsed json file to folder
    # create class DirManager in config, which is called on ConfigManager.setup()
    # which creates all necessary folders on setup
    # DirManager will also have specific functions to read/write files
    # from those necessary folders
    if "error" in parsed_json.keys():
        return gr.update(value=parsed_json), gr.update(visible=False)

    file_name = os.path.basename(file_path)

    return gr.update(
        value={"success": "Workflow imported - " + str(file_name)}
    ), gr.update(visible=False)


def workflow_importer_ui():
    gr.Markdown("## Import Workflow")

    workflow_upload = gr.File(type="filepath", file_types=[".json"], label="JSON File")
    import_button = gr.Button("Import Workflow", interactive=True, visible=False)
    code_display = gr.JSON(
        label="Imported Workflow",
        container=True,
        value={"workflow": "Import you workflow and visualize it here."},
        elem_classes=["skdv_json_display"],
    )

    workflow_upload.upload(
        fn=on_workflow_upload,
        inputs=workflow_upload,
        outputs=[code_display, import_button],
    )

    import_button.click(
        fn=on_workflow_import,
        inputs=workflow_upload,
        outputs=[code_display, import_button],
    )
