
from cioblender import software, util

def resolve_payload(**kwargs):
    """Resolve the payload for the environment."""

    # Get unique paths from packages with non-empty 'path' attribute
    paths = list({package.get("path") for package in software.packages_in_use(**kwargs) if package.get("path")})

    # Join the unique paths with ":"
    blender_path = ":".join(paths)

    # Todo: do we need to add the other paths?
    # blender_path = ":".join([blender_path, "/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin"])

    # Define a dictionary for environment variables
    env_dict = {
        "PATH": blender_path,
        # "CONDUCTOR_PATHHELPER": "0",
        # "HDF5_USE_FILE_LOCKING": "FALSE",
        # "__conductor_letter_drives__": "1"
    }
    try:
        extra_variables = kwargs.get("extra_variables", None)
        #for i, variable in enumerate(extra_variables):
        #    print(i, variable.variable_name, variable.variable_value)

        if extra_variables:
            for variable in extra_variables:
                key, value = variable.variable_name, variable.variable_value
                if key and value:
                    env_dict[key] = value
    except Exception as e:
        print ("Unable to get extra environment variables. Error: {}".format(e))
        pass


    return {"environment": env_dict}