
import re

#XPY = hou.exprLanguage.Python

from cioseq.sequence import Sequence

AUTO_RX = re.compile(r"^auto[, :]+(\d+)$")
FML_RX = re.compile(r"^fml[, :]+(\d+)$")

EXPR = """
import hou
from cioseq.sequence import Sequence

rop = hou.node(hou.pwd().parm('driver_path').evalAsString())
if not rop:
    first, last = hou.playbar.timelineRange()
    inc = hou.playbar.frameIncrement()
    return str(Sequence.create( first, last, inc))

use_range = rop.parm("trange").eval()
if not use_range:
    return int(hou.frame())

progression = rop.parmTuple("f").eval()
return str(Sequence.create(*progression))
"""


def on_use_custom(node, **kwargs):
    """
    Whether to override the frames specified in the input ROP.
    """
    node.parm("frame_spec").deleteAllKeyframes()
    #if not node.parm("use_custom_frames").eval():
    #    node.parm("frame_spec").setExpression(EXPR, XPY, True)


def set_stats_panel(node, **kwargs):
    """
    Update fields in the stats panel that are driven by frames related setttings.
    """
    if node.parm("is_sim").eval():
        node.parm("scout_frame_spec").set("0")
        node.parmTuple("frame_task_count").set((1, 1))
        node.parmTuple("scout_frame_task_count").set((0, 0))
        return

    main_seq = main_frame_sequence(**kwargs)
    frame_count = len(main_seq)
    task_count = main_seq.chunk_count()

    scout_seq = scout_frame_sequence(main_seq, **kwargs)

    scout_frame_count = frame_count
    scout_task_count = task_count
    scout_frame_spec = "No scout frames. All frames will be started."
    if scout_seq:
        scout_chunks = main_seq.intersecting_chunks(scout_seq)
        # if there are no intersecting chunks, there are no scout frames, which means all frames will start.
        if scout_chunks:
            scout_tasks_sequence = Sequence.create(",".join(str(chunk) for chunk in scout_chunks))
            scout_frame_count = len(scout_tasks_sequence)
            scout_task_count = len(scout_chunks)
            scout_frame_spec = str(scout_seq)

    node.parm("scout_frame_spec").set(scout_frame_spec)
    node.parmTuple("frame_task_count").set((frame_count, task_count))
    node.parmTuple("scout_frame_task_count").set((scout_frame_count, scout_task_count))


def main_frame_sequence(**kwargs):
    """
    Generate Sequence containing current chosen frames.
    """
    chunk_size = kwargs.get("chunk_size")
    spec = kwargs.get("frame_spec")
    if not spec:
        return Sequence.create(1, 1)
    else:
        return Sequence.create(spec, chunk_size=chunk_size, chunk_strategy="progressions")


def scout_frame_sequence(main_sequence, **kwargs):
    """
    Generate Sequence containing scout frames.

    Scout frames may be generated from a spec, such as 1-2, 5-20x3 OR by subsampling the main
    sequence. Example: auto:5 would generate a scout sequence of 5 evenly spaced frames in the main
    sequence.
    """
    if not kwargs.get("use_scout_frames"):
        return

    scout_spec = kwargs.get("scout_frames")

    match = AUTO_RX.match(scout_spec)
    if match:
        samples = int(match.group(1))
        return main_sequence.subsample(samples)
    else:
        match = FML_RX.match(scout_spec)
        if match:
            samples = int(match.group(1))
            return main_sequence.calc_fml(samples)

    try:
        return Sequence.create(scout_spec).intersection(main_sequence)

        #  Sequence.create(scout_spec)
    except:
        pass


def resolve_payload(**kwargs):
    # Todo: fix this.
    # If we are in sim mode, don't add scout frames.
    # if node.parm("is_sim").eval():
    #    return {}
    # If we are not using scout frames, don't add them.
    use_scout_frames = kwargs.get("use_scout_frames")
    if not use_scout_frames:
        return {}

    main_seq = main_frame_sequence(**kwargs)
    scout_sequence = scout_frame_sequence(main_seq, **kwargs)
    if scout_sequence:
        return {"scout_frames": ",".join([str(f) for f in scout_sequence])}
    return {}
