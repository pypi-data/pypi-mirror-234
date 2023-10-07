

import bpy
import traceback
from bpy.utils import register_class, unregister_class
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, CollectionProperty


from ciocore import conductor_submit

job_msg = "Job submitted."

from cioblender import (
    payload,
    project,
    instances,
    controller,
    software,
    submit,
    # util,
)
#from cioblender.submission_dialog import SubmissionDialog

import json
import os

bl_info = {
    "name": "Conductor Render Submitter",
    "author": "Your Name",
    "version": (0, 1),
    "blender": (3, 5, 1),
    "location": "Render > Properties",
    "description": "Render submitter UI for Conductor",
    "category": "Render",
}

bpy.types.Object.my_int_property = bpy.props.IntProperty(
    name="My Int Property",
    description="This is a custom integer property for the object",
    default=70,    # Default initial value
    min=0,        # Minimum value for the slider
    max=100,       # Maximum value for the slider
)

class ObjPanel(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_category = "Conductor Render Submitter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene


class RenderSubmitterPanel(ObjPanel):
    bl_label = "Conductor Render Submitter"
    bl_idname = "RENDER_PT_RenderSubmitterPanel"


class ConductorJobPanel(ObjPanel):
    bl_label = "Conductor Job"
    bl_idname = "RENDER_PT_ConductorJobPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Connect button
        layout.operator("render_submitter.connect", text="Connect")
        # Export Script button
        layout.operator("render_submitter.export_script", text="Export Script")
        # Submit button
        layout.operator("render_submitter.submit", text="Submit")


class ProgressPanel(Panel):
    bl_label = "Progress"
    bl_idname = "OBJECT_PT_progress"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        #layout.prop(scene, "job_progress", slider=True, index=1, text="Job Progress")
        #layout.prop(scene, "computing_md5", slider=True, index=2, text="Computing MD5")
        #layout.prop(scene, "file_upload", slider=True, index=1, text="File Upload")


class ConfigurationPanel(ObjPanel):
    bl_label = "Configuration"
    bl_idname = "RENDER_PT_ConfigurationPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"

class GeneralPanel(ObjPanel):
    bl_label = "General"
    bl_idname = "RENDER_PT_GeneralPanel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Job Title:")
        layout.prop(scene, "job_title", text="")

        layout.label(text="Project:")
        layout.prop(scene, "project", text="")

        layout.label(text="Instance Type:")
        layout.prop(scene, "instance_type", text="")
        #layout.operator("general.instance_type", text="")

        layout.label(text="Machine Type:")
        layout.prop(scene, "machine_type", text="")

        #layout.label(text="Preemptible:")
        layout.prop(scene, "preemptible", text="Preemptible")

        layout.label(text="Preemptible Retries:")
        layout.prop(scene, "preemptible_retries", text="")

        layout.label(text="Blender Version:")
        layout.prop(scene, "blender_version", text="")

        layout.label(text="Render Software:")
        layout.prop(scene, "render_software", text="")

        # Todo: Add a button to add a plugin
        # layout.operator("render_submitter.add_plugin", text="Add Plugin")


# FramesPanel class
class FramesPanel(ObjPanel):
    bl_label = "Frames"
    bl_idname = "RENDER_PT_Conductor_Frames_Panel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Chunk Size:")
        layout.prop(scene, "chunk_size", text="")

        #layout.label(text="Override Frame Range:")
        #layout.prop(scene, "override_frame_range", text="Override Frame Range")

        layout.label(text="Frame Spec:")
        layout.prop(scene, "frame_spec", text="")

        # Display the option to use scout frames
        #layout.label(text="Use Scout Frames:")
        layout.prop(scene, "use_scout_frames", text="Use Scout Frames")

        layout.label(text="Scout Frames:")
        layout.prop(scene, "scout_frames", text="")


class StatsPanel(ObjPanel):
    bl_label = "Stats"
    bl_idname = "RENDER_PT_Conductor_Stats_Panel"
    bl_parent_id = "RENDER_PT_ConfigurationPanel"
    def draw(self, context):
        self.layout.row().label(text="") # blank line

class AdvancedPanel(ObjPanel):
    bl_label = "Advanced"
    bl_idname = "RENDER_PT_Conductor_Advanced_Panel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row().label(text="") # blank line
        layout.prop(scene, "output_folder", text="Output Folder")

# Define a custom panel class
class ExtraAssetProperty(PropertyGroup):
    file_path: StringProperty(
        name="File Path",
        description="Path to extra asset file",
        subtype='FILE_PATH',
    )

class ExtraAssetsPanel(Panel):
    bl_label = "Extra Assets"
    bl_idname = "RENDER_PT_ExtraAssetsPanel"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        # Add a button to open the file browser
        layout.operator("object.open_file_browser")

        # Access the extra_assets_list from the scene
        scene = context.scene
        extra_assets_list = scene.extra_assets_list

        for i, extra_asset in enumerate(extra_assets_list):
            row = layout.row(align=True)
            row.prop(extra_asset, "file_path", text="File Path", slider=True)

class RemoveExtraAssetOperator(Operator):
    bl_idname = "custom.remove_extra_asset"
    bl_label = "Remove Extra Asset"
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        extra_assets_list = scene.extra_assets_list
        extra_assets_list.remove(self.index)
        return {'FINISHED'}

class OpenFileBrowserOperator(Operator):
    bl_idname = "object.open_file_browser"
    bl_label = "Add Extra Asset"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select a file:")

    def execute(self, context):
        # Check if the selected file path is not empty
        if self.filepath:
            # Add the selected file as an instance of ExtraAssetProperty
            scene = context.scene
            if not hasattr(scene, "extra_assets_list"):
                scene.extra_assets_list = []

            extra_asset = scene.extra_assets_list.add()
            extra_asset.file_path = self.filepath

            # Refresh the UI
            refresh_ui()

        return {'FINISHED'}

class PreviewPanel(ObjPanel):
    bl_label = "Preview"
    bl_idname = "RENDER_PT_PreviewPanel"
    bl_parent_id = "RENDER_PT_RenderSubmitterPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Get all item values as JSON format
        values = create_json_data()

        # Convert values to JSON format
        json_data = json.dumps(values, indent=4)
        #json_data = values

        # Display the JSON format line by line in the preview panel
        lines = json_data.split("\n")
        for line in lines:
            layout.label(text=line)

# Connect Operator
class ConnectOperator(Operator):
    bl_idname = "render_submitter.connect"
    bl_label = "Connect"

    def execute(self, context):
        # Connect to Conductor logic here
        print("Connecting to Conductor...")
        controller.connect("render_submitter.connect")

        # Update other property menus here if needed
        populate_project_menu(context)
        populate_blender_version_menu(context)
        populate_instance_type_menu(context)
        populate_output_folder(context)
        populate_extra_env(context)
        # populate_render_software_menu(context)

        # Get blender filename
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        print("Filename: ", filename)
        filename = filename.split(".")[0]
        # Get blender version
        blender_version = bpy.app.version_string.split(" ")[0]
        print("Blender Version: ", blender_version)

        # Set the job title
        software_version = bpy.app.version
        software_version = f"{software_version[0]}.{software_version[1]}.{software_version[2]}"
        job_title = "Blender {} Linux Render {}".format(software_version, filename)

        # Set bpy.types.Scene.job_title to job_title
        context.scene.job_title = job_title  # Update the job_title property
        # Set the use_scout_frames property to True
        context.scene.use_scout_frames = True
        context.scene.frame_spec = get_scene_frame_range()

        return {'FINISHED'}


# Submit Operator
class ExportScriptOperator(Operator):
    bl_idname = "render_submitter.export_script"
    bl_label = "Export Script"

    def execute(self, context):
        print("Export Script clicked")

        # Get all item values as JSON data
        json_data = json.dumps(create_json_data(), indent=4)
        print("JSON Data:\n", json_data)

        # Save JSON data to a file
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = filename.split(".")[0]
        filepath = os.path.join(bpy.path.abspath("//"), f"{filename}.json")
        with open(filepath, "w") as file:
            file.write(json_data)

        # Open the file manager in Blender to save the JSON file
        bpy.ops.wm.path_open(filepath=filepath)

        return {'FINISHED'}
# Submit Operator
class SubmitOperator(Operator):
    bl_idname = "render_submitter.submit"
    bl_label = "Submit"

    def execute(self, context):
        print("Submit clicked")

        kwargs = create_raw_data()
        # print("scene data is: ", kwargs)
        blender_payload = payload.resolve_payload(**kwargs)
        # print("blender_payload is: ", blender_payload)

        # Show the Submission dialog
        #Todo: Finish the progress tabs: Add fourth row
        submit.invoke_submission_dialog(blender_payload)

        # result = submit_job(blender_payload)
        # print("Submission result is: ", result)

        return {'FINISHED'}
# RenderAddPluginOperator class
class RenderAddPluginOperator(Operator):
    bl_idname = "render_submitter.add_plugin"
    bl_label = "Add Plugin"

    def execute(self, context):
        # Add Plugin logic
        self.report({'INFO'}, "Plugin added successfully")
        return {'FINISHED'}


# Define the class for the SimpleOperator
class SimpleOperator(bpy.types.Operator):
    bl_idname = "custom.simple_operator"
    bl_label = "Custom Notification Operator"

    success = bpy.props.BoolProperty(default=False)
    job_number = bpy.props.StringProperty(default="")

    def execute(self, context):
        if self.success:
            self.report({'INFO'}, f"Job {self.job_number} was successful.")
        else:
            self.report({'ERROR'}, f"Job {self.job_number} failed.")
        return {'FINISHED'}

class ExtraEnvironmentPanel(bpy.types.Panel):

    bl_label = "Extra Environment Panel"
    bl_idname = "RENDER_PT_ExtraEnvironment"
    bl_parent_id = "RENDER_PT_Conductor_Advanced_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        # Add a button to add a new variable row
        layout.operator("custom.add_variable")

        # Draw existing variables
        scene = context.scene
        variables = scene.custom_variables.variables
        for i, variable in enumerate(variables):
            row = layout.row()
            row.prop(variable, "variable_name", text="Variable")
            row.prop(variable, "variable_value", text="Value")
            row.operator("custom.remove_variable", text="", icon='X').index = i

# Define an operator to add a new variable row
class AddVariableOperator(bpy.types.Operator):
    bl_idname = "custom.add_variable"
    bl_label = "Add Extra Environment Variable"

    def execute(self, context):
        scene = context.scene
        variables = scene.custom_variables.variables
        variables_dict = scene.variables_dict
        new_variable = variables.add()
        new_variable.variable_name = ""
        new_variable.variable_value = ""
        variables_dict[new_variable.variable_name] = new_variable.variable_value
        return {'FINISHED'}


# Define an operator to remove a variable row
class RemoveVariableOperator(bpy.types.Operator):
    bl_idname = "custom.remove_variable"
    bl_label = "Remove Variable"
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        variables = scene.custom_variables.variables
        variables_dict = scene.variables_dict
        variable = variables[self.index]
        key = variable.variable_name
        if key in variables_dict:
            del variables_dict[key]
        variables.remove(self.index)
        return {'FINISHED'}

# Define a custom property for storing variable data
class CustomVariableProperty(bpy.types.PropertyGroup):
    variable_name: bpy.props.StringProperty(name="Variable Name")
    variable_value: bpy.props.StringProperty(name="Variable Value")

# Define a custom property to store the list of variables
class CustomVariableListProperty(bpy.types.PropertyGroup):
    variables: bpy.props.CollectionProperty(type=CustomVariableProperty)

def populate_extra_env(context):
    # Todo: review these hard coded env variables
    # Populate extra env variables
    env_dict = {
        "CONDUCTOR_PATHHELPER": "0",
        "HDF5_USE_FILE_LOCKING": "FALSE",
        "__conductor_letter_drives__": "1"
    }
    scene = context.scene
    variables = scene.custom_variables.variables
    variables_dict = scene.variables_dict
    for key, value in env_dict.items():
        if key not in variables_dict:
            new_variable = variables.add()
            new_variable.variable_name = key
            new_variable.variable_value = value
            variables_dict[key] = value

def refresh_ui():
    """Refresh the UI"""
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def submit_job(payload):
    """Submit a job to Conductor."""
    try:
        remote_job = conductor_submit.Submit(payload)
        response, response_code = remote_job.main()

    except:
        response = traceback.format_exc()
        response_code = 500

    print("response is: ", response)

    return {"response": response, "response_code": response_code}

def get_job_message(self, context):
    if job_msg:
        self.layout.label(text=job_msg)

# Update the Machine Type Menu based on the value of the Instance Type Menu
def update_instance_type_menu(self, context):
    # Print the new value of the Instance Type Menu
    print("Instance Type:", context.scene.instance_type)

    # Update the Machine Type Menu based on the value of the Instance Type Menu
    instance_list = instances.populate_menu(context.scene.instance_type)
    # print("New Instance List: ", instance_list)

    # Update the items of the Machine Type Menu
    bpy.types.Scene.machine_type = bpy.props.EnumProperty(
        name="Machine Type",
        items=instance_list
    )

def populate_project_menu(context):
    """Populate the Project Menu"""
    # print("Populate the Project Menu ...")
    project_items = project.populate_menu(bpy.types.Scene)
    # Reverse the list
    project_items.reverse()
    # print("project_items: ", project_items)
    bpy.types.Scene.project = bpy.props.EnumProperty(
        name="project",
        items=project_items
    )

def populate_blender_version_menu(context):
    """Populate the Blender Version Menu """
    # print("Populate the Blender Version Menu ...")
    blender_versions = software.populate_host_menu()
    # Reverse the list
    blender_versions.reverse()
    # print("blender_versions: ", blender_versions)
    bpy.types.Scene.blender_version = bpy.props.EnumProperty(
        name="Blender Version",
        items=blender_versions
    )

def populate_instance_type_menu(context):
    """Populate the Instance Type Menu """
    print("Populate the Instance Type Menu ...")
    instance_list = instances.populate_menu(context.scene.instance_type)
    # print("instance list:", instance_list)
    bpy.types.Scene.machine_type = bpy.props.EnumProperty(
        name="Machine Type",
        items=instance_list
    )
def populate_output_folder(context):
    scene = bpy.context.scene
    blender_filepath = bpy.context.blend_data.filepath
    blender_folder = os.path.dirname(blender_filepath)
    output_folder = get_output_folder(blender_folder)
    scene.output_folder = output_folder


# Todo: fix this
def populate_render_software_menu(context):
    """Populate the Render Software Menu """
    print("Populate the Render Software Menu ...")
    kwargs = create_raw_data()
    render_software = software.populate_driver_menu(**kwargs)
    print("render_software: ", render_software)
    bpy.types.Scene.render_software = bpy.props.EnumProperty(
        name="Render Software",
        items=render_software
    )


def create_raw_data():
    #
    scene = bpy.context.scene
    software_version = bpy.app.version
    software_version = f"{software_version[0]}.{software_version[1]}.{software_version[2]}"

    start_frame = scene.frame_start
    end_frame = scene.frame_end
    frame_range = "{}-{}".format(start_frame, end_frame)

    # Get the full path to the Blender file
    blender_filepath = bpy.context.blend_data.filepath
    # Get the Blender filename from the full path
    blender_filename = bpy.path.basename(blender_filepath)
    # Get the folder containing the Blender file
    blender_folder = os.path.dirname(blender_filepath)

    kwargs = {
        "software_version": software_version,
        "job_title": scene.job_title,
        "project": scene.project,
        "instance_type": scene.instance_type,
        "machine_type": scene.machine_type,
        "preemptible": scene.preemptible,
        "preemptible_retries": scene.preemptible_retries,
        "blender_version": scene.blender_version,
        "render_software": scene.render_software,
        "chunk_size": scene.chunk_size,
        "scene_frame_start": scene.frame_start,
        "scene_frame_end": scene.frame_end,
        "frame_range": frame_range,
        "frame_spec": scene.frame_spec,
        "use_scout_frames": scene.use_scout_frames,
        "scout_frames": scene.scout_frames,
        "output_folder": scene.output_folder,
        "blender_filename": blender_filename,
        "blender_filepath": blender_filepath,
        "blender_folder": blender_folder,
        "extra_variables": scene.custom_variables.variables,

    }
    return kwargs

def get_output_folder(blender_folder):
    """Get the output folder"""
    output_folder = "~/render"
    try:
        if not blender_folder:
            blender_folder = os.path.expanduser("~")
            output_folder = os.path.join(blender_folder, "render")

        else:
            output_folder = os.path.join(blender_folder, "render")

    except Exception as e:
        print("Error creating output folder: ", e)
        pass

    # create the output folder if it doesn't exist
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder


def create_json_data():
    """Create JSON data from the scene properties"""
    kwargs = create_raw_data()
    json_data = payload.resolve_payload(**kwargs)
    # print("json_data: ", json_data)
    return json_data

def get_scene_frame_range():
    """Get the frame range from the scene"""
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    frame_range = "{}-{}".format(start_frame, end_frame)
    return frame_range


# List of classes to register
classes = [
    RenderSubmitterPanel, # Grandparent panel
    ConductorJobPanel, # Parent panel
    ConfigurationPanel, # Parent panel
    AdvancedPanel, # Parent panel
    PreviewPanel, # Parent panel
    GeneralPanel, # Child panel
    FramesPanel, # Child panel
    ExtraAssetsPanel,# Child panel
    OpenFileBrowserOperator,# Child panel
    RemoveExtraAssetOperator,
    ExtraEnvironmentPanel,# Child panel
    ExtraAssetProperty,
    AddVariableOperator,
    RemoveVariableOperator,
    CustomVariableProperty,
    CustomVariableListProperty,
    ConnectOperator,
    ExportScriptOperator,
    SubmitOperator,
    RenderAddPluginOperator,
    SimpleOperator,
]

# Register the add-on
def register():
    for cls in classes:
        register_class(cls)

    # Create custom properties for the scene
    bpy.types.Scene.job_title = bpy.props.StringProperty(name="Job Title", default="Blender Linux Render")
    bpy.types.Scene.project = bpy.props.StringProperty(name="project", default="default")
    bpy.types.Scene.instance_type = bpy.props.EnumProperty(
        name="Instance Type",
        items=[("CPU", "CPU", ""), ("GPU", "GPU", "")],
        update=update_instance_type_menu
    )

    bpy.types.Scene.machine_type = bpy.props.EnumProperty(
        name="Machine Type",
        #items=instance_list
        items=[]
    )

    bpy.types.Scene.preemptible = bpy.props.BoolProperty(name="Preemptible", default=True)
    bpy.types.Scene.preemptible_retries = bpy.props.IntProperty(name="Preempted Retries", default=1)

    bpy.types.Scene.blender_version = bpy.props.EnumProperty(
        name="Blender Version",
        items=[]
    )

    bpy.types.Scene.render_software = bpy.props.EnumProperty(
        name="Render Software",
        items = [("Cycles", "Cycles", ""), ("Eevee", "Eevee", "")]
    )

    bpy.types.Scene.chunk_size = bpy.props.IntProperty(name="Chunk Size", default=1)

    bpy.types.Scene.frame_spec = bpy.props.StringProperty(name="Frame Spec", default="1-100")
    bpy.types.Scene.use_scout_frames = bpy.props.BoolProperty(name="Use Scout Frames", default=True)
    bpy.types.Scene.scout_frames = bpy.props.StringProperty(name="Scout Frames", default="fml:3")

    bpy.types.Scene.extra_assets_list = CollectionProperty(type=ExtraAssetProperty)

    bpy.types.Scene.custom_variables = bpy.props.PointerProperty(type=CustomVariableListProperty)
    bpy.types.Scene.variables_dict = {}
    bpy.types.Scene.output_folder = bpy.props.StringProperty(name="Output Folder", description="", default="")


# Unregister the add-on
def unregister():
    for cls in reversed(classes):
       bpy.utils.unregister_class(cls)
    del bpy.types.Scene.extra_assets_list

# Run the register function when the add-on is enabled
if __name__ == "__main__":
    # Register the add-on
    register()
    # Switch to the rendering workspace to show the UI
    bpy.context.window.workspace = bpy.data.workspaces["Render"]
