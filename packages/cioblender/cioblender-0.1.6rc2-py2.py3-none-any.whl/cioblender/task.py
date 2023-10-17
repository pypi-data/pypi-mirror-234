
from cioblender import frames, util

renderer_dict = {
    "Cycles": "CYCLES",
    "Eevee": "BLENDER_EEVEE",
}
def get_task_template(**kwargs):
    first = kwargs.get("first", 1)
    last = kwargs.get("last", 1)
    step = kwargs.get("step", 1)
    blender_scene_path = kwargs.get("blender_filepath", None)
    blender_scene_path = util.clean_and_strip_path(blender_scene_path)
    output_folder = kwargs.get("output_folder", None)
    output_folder = util.clean_and_strip_path(output_folder)
    blender_filename = kwargs.get("blender_filename", None)
    if blender_filename:
        blender_filename = blender_filename.split(".")[0]
    render_software = kwargs.get("render_software", None)
    render_software = renderer_dict.get(render_software, "CYCLES")
    cmd = "blender -b --enable-autoexec {} -E {} --render-output {}/{}_ -s {} -e {} -a".format(
        blender_scene_path, render_software, output_folder, blender_filename, first, last)
    return cmd
def resolve_payload(**kwargs):
    """
    Resolve the task_data field for the payload.

    If we are in sim mode, we emit one task.
    """
    frame_range = kwargs.get("frame_spec", None)

    tasks = []
    sequence = frames.main_frame_sequence(**kwargs)
    chunks = sequence.chunks()
    # Get the scout sequence, if any.
    for i, chunk in enumerate(chunks):
        # Get the frame range for this chunk.
        kwargs["first"] = chunk.start
        kwargs["last"] = chunk.end
        kwargs["step"] = chunk.step
        # Get the task template.
        cmd = get_task_template(**kwargs)


        tasks.append({"command": cmd, "frames": str(chunk)})


    return {"tasks_data": tasks}