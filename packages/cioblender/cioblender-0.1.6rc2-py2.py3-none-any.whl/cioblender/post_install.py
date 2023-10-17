import os
import sys
import shutil

def fslash(path):
    return path.replace("\\", "/")

PLATFORM = sys.platform
PWD = os.path.dirname(os.path.abspath(__file__))
CIO_DIR = fslash(os.path.dirname(PWD))

ADDOON_FILE = os.path.join(PWD, "conductor_submitter_plugin.py")


INIT_CONTENT = """
import sys
CIO_DIR = "{}"
sys.path.insert(1, CIO_DIR)
""".format(CIO_DIR)

def copy_plugin_to_blender_folders(platform):
    user_home = os.path.expanduser("~")
    blender_versions_folder = None
    copied_folders = []
    addon_destination = ""
    try:
        if platform.startswith("win"):
            blender_versions_folder = os.path.join(user_home, "AppData/Roaming/Blender Foundation/Blender")
        elif platform.startswith("linux"):
            blender_versions_folder = os.path.join(user_home, ".config/blender")
        elif platform.startswith("darwin"):
            blender_versions_folder = os.path.join(user_home, "Library/Application Support/Blender")

        if blender_versions_folder:
            for version_folder in os.listdir(blender_versions_folder):
                addon_folder = os.path.join(blender_versions_folder, version_folder, "scripts/addons")
                if os.path.exists(addon_folder):
                    addon_destination = os.path.join(addon_folder, "conductor_submitter_plugin.py")
                    shutil.copy(ADDOON_FILE, addon_destination)
                    copied_folders.append(addon_folder)
    except Exception as e:
        print("Unable to copy plugin {} to folder {}, error: {}", ADDOON_FILE, addon_destination, e)
        pass

    return copied_folders

def add_submitter_header():
    """Add the CIO_DIR path to the beginning of the addon file.
    Make sure to strip existing line endings and add macOS-style "\n" endings.
    """
    with open(ADDOON_FILE, "r", encoding="utf-8") as f:
        old_lines = f.readlines()  # read old content

    with open(ADDOON_FILE, "w", encoding="utf-8") as f:
        f.write(INIT_CONTENT + "\n")  # write new content at the beginning
        for line in old_lines:  # write old content after new
            f.write(line.rstrip('\r\n') + "\n")  # strip existing line endings and add macOS-style "\n" endings


def main():
    if not PLATFORM.startswith(("win", "linux", "darwin")):
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)

    add_submitter_header()
    copied_folders = copy_plugin_to_blender_folders(PLATFORM)

    if copied_folders:
        sys.stdout.write("Copied Conductor Blender plugin to the following folders:\n")
        for folder in copied_folders:
            sys.stdout.write(folder + "\n")
        sys.stdout.write("Completed Blender addon setup!\n")
    else:
        sys.stderr.write("No Blender addon folders found.\n")

if __name__ == "__main__":
    main()
