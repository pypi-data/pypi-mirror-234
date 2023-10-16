import bpy
import os

from cioblender import util
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
from ciopath.gpath import Path

def resolve_payload(**kwargs):
    """
    Resolve the upload_paths field for the payload.

    """
    path_list = PathList()

    path_list.add(*auxiliary_paths(**kwargs))
    path_list.add(*extra_paths())
    # Todo: test scan_assets further
    path_list.add(*scan_assets())

    return {"upload_paths": [p.fslash() for p in path_list]}

def auxiliary_paths(**kwargs):
    """ Get auxiliary paths"""
    path_list = PathList()
    try:
        blender_filepath = kwargs.get("blender_filepath")
        blender_filepath = blender_filepath.replace("\\", "/")
        if blender_filepath and "startup.blend" not in blender_filepath:
            # Check if blender_filepath exists
            if os.path.exists(blender_filepath):
                path_list.add(blender_filepath)
            else:
                print("Unable to find blender_filepath: {}".format(blender_filepath))
    except Exception as e:
        print("Unable to load auxiliary paths, error: {}".format(e))
    return path_list


def extra_paths():
    """Add extra assets"""
    path_list = PathList()
    try:
        scene = bpy.context.scene
        extra_assets_list = scene.extra_assets_list

        for asset in extra_assets_list:
            if asset.file_path and "startup.blend" not in asset.file_path:
                # Check if asset.file_path exists
                if os.path.exists(asset.file_path):
                    path_list.add(asset.file_path)
                else:
                    print("Unable to find extra asset: {}".format(asset.file_path))
    except Exception as e:
        print("Unable to load extra assets, error: {}".format(e))

    return path_list

# Modify the scan_assets function to include the whole filepath
def scan_assets(**kwargs):
    path_list = PathList()

    try:
        # Iterate through all materials in the scene
        for material in bpy.data.materials:
            if material.node_tree:
                for node in material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        image_filepath = bpy.path.abspath(node.image.filepath)
                        # check if the image_filepath exists
                        if os.path.exists(image_filepath):
                            path_list.add(image_filepath)
                        else:
                            print("Unable to find image_filepath: {}".format(image_filepath))

        # Iterate through all objects in the scene
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material and slot.material.use_nodes:
                        for node in slot.material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image:
                                image_filepath = bpy.path.abspath(node.image.filepath)
                                # check if the image_filepath exists
                                if os.path.exists(image_filepath):
                                    path_list.add(image_filepath)
                                else:
                                    print("Unable to find image_filepath: {}".format(image_filepath))

        # Iterate through all linked libraries
        for library in bpy.data.libraries:
            # Check if the library is linked or used in the scene
            if library.users > 0:
                library_filepath = bpy.path.abspath(library.filepath)
                # check if the library_filepath exists
                if os.path.exists(library_filepath):
                    path_list.add(library_filepath)
                else:
                    print("Unable to find library_filepath: {}".format(library_filepath))

    except Exception as e:
        print("Unable to scan assets: {}".format(e))
        pass

    return path_list
