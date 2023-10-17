"""
Manage 3 software categories:

1. Remote Blender version.
2. Plugin for the connected driver.
3. Extra plugins.


"""


from ciocore import data as coredata
from cioblender import driver


def populate_host_menu():
    """Populate Blender version menu.

    This is called by the UI whenever the user clicks the Houdini Version button.
    """
    if not coredata.valid():
        return ["not_connected", "-- Not connected --"]

    software_data = coredata.data()["software"]
    host_names = software_data.supported_host_names()
    if not host_names:
        return [("no_host_names", "-- No hostnames --", "")]
    else:
        # Create a dictionary of projects
        blender_host_names = {}
        # For each host in the host_names, if the host is not in the blender_host_names dictionary,
        # add it to the dictionary
        for s in host_names:
            if s not in blender_host_names:
                blender_host_names[s] = (s, s, "")
        # Return the list of hosts
        return list(blender_host_names.values())


    # hostnames will have the platform specifier. We want to strip the platform.
    #return [el for i in host_names for el in (i," ".join(i.split()[:2]).capitalize() )]


def populate_driver_menu(**kwargs):
    """Populate renderer/driver type menu.
    """
    if not coredata.valid():
        return ["not_connected", "-- Not connected --"]

    return [el for i in _get_compatible_plugin_versions(**kwargs) for el in (i,i)]

def populate_extra_plugin_menu(node):
    if not coredata.valid():
        return ["not_connected", "-- Not connected --"]

    _get_all_plugin_versions
    return [el for i in _get_all_plugin_versions(node) for el in (i,i)]

def ensure_valid_selection(**kwargs):
    """
    If connected, ensure the value of this parm is valid.
    """
    if not coredata.valid():
        return

    software_data = coredata.data()["software"]
    host_names = software_data.supported_host_names()
    selected_host = kwargs.get("host_version")

    if not host_names:
        kwargs["host_version"] = "no_houdini_packages"
        kwargs["driver_version"] = "no_drivers"
        num_plugins = kwargs.get("extra_plugins")
        for i in range(1, num_plugins+1):
            kwargs["extra_plugin_{}".format(i)] = "no_plugins"
        return

    if selected_host not in host_names:
        selected_host = host_names[-1]
    kwargs["host_version"] = selected_host
    
    update_driver_selection(**kwargs)
    update_plugin_selections(**kwargs)


    driver_names = _get_compatible_plugin_versions(**kwargs)

    if not driver_names:
        kwargs["driver_version"] = "no_drivers"

        return
    selected_driver = kwargs.get("driver_version")


    if selected_driver not in driver_names:
        selected_driver = driver_names[-1]

    kwargs["driver_version"] = selected_driver

def _get_compatible_plugin_versions(**kwargs):
    
    driver_data = driver.get_driver_data(**kwargs)
    if driver_data["conductor_product"].lower().startswith(("built-in", "unknown")):
        return [driver_data["conductor_product"]]

    if not coredata.valid():
        return []
    software_data = coredata.data().get("software")
    selected_host = kwargs.get("host_version")
    plugins = software_data.supported_plugins(selected_host)
    plugin_names = [plugin["plugin"] for plugin in plugins]

    if driver_data["conductor_product"] not in plugin_names:
        return ["No plugins available for {}".format(driver_data["conductor_product"])]

    plugin_versions = []
    for plugin in plugins:
        if plugin["plugin"] == driver_data["conductor_product"]:
            for version in plugin["versions"]:
                plugin_versions.append("{} {}".format(
                    plugin["plugin"], version))
            break
    
    return plugin_versions



def _get_all_plugin_versions(**kwargs):
    
    if not coredata.valid():
        return []
    software_data = coredata.data().get("software")
    selected_host = kwargs.get("host_version")
    plugins = software_data.supported_plugins(selected_host)

    plugin_versions = []
    for plugin in plugins:
        for version in plugin["versions"]:
            plugin_versions.append("{} {}".format(
                plugin["plugin"], version))

    return plugin_versions


def update_driver_selection(node, **kwargs):
    """Update the driver selection to be compatible with the host selection."""
    selected_plugin = kwargs.get("driver_version")

    plugin_names = _get_compatible_plugin_versions(**kwargs)
    if not plugin_names:
        kwargs["driver_version"] = "no_plugins_available"
        return
    if selected_plugin not in plugin_names:
        kwargs["driver_version"] = plugin_names[0]

def update_plugin_selections(node, **kwargs):

    plugin_names = _get_all_plugin_versions(**kwargs)
    num_plugins = kwargs.get("extra_plugins")
    for i in range(1, num_plugins+1):
        selected_plugin = kwargs.get("extra_plugin_{}".format(i))
        if not plugin_names:
            kwargs["extra_plugin_{}".format(i)] = "no_plugins_available"
            continue
        if selected_plugin not in plugin_names:
            kwargs["extra_plugin_{}".format(i)] = plugin_names[0]

# TODO: This is a temporary function to resolve the package IDs for the given node.
def resolve_payload(**kwargs):
    """Resolve the package IDs section of the payload for the given node."""
    ids = set()

    # print("packages: {}".format(packages_in_use(**kwargs)))
    for package in packages_in_use(**kwargs):
        ids.add(package["package_id"])

    return {"software_package_ids": list(ids)}

#Todo fix this
def packages_in_use(**kwargs):
    """Return a list of packages as specified by names in the software dropdowns.
    """
    if not coredata.valid():
        return []
    tree_data = coredata.data().get("software")
    #print("tree_data: {}".format(tree_data))
    if not tree_data:
        return []

    platform = list(coredata.platforms())[0]
    # print("platform: {}".format(platform))
    host = kwargs.get("blender_version")
    blender_version = kwargs.get("blender_version")
    driver = "{}/{} {}".format(host, blender_version, platform)
    # print("driver: {}".format(driver))
    paths = [host, driver]
    # print("paths: {}".format(paths))
    num_plugins = kwargs.get("extra_plugins", 0)
    for i in range(1, num_plugins+1):
        parm_val = kwargs["extra_plugin_{}".format(i)]
        paths.append("{}/{} {}".format(host, parm_val, platform))

    return list(filter(None, [tree_data.find_by_path(path) for path in paths if path]))


def add_plugin(node, **kwargs):
    """Add a new variable to the UI.
    
    This is called by the UI when the user clicks the Add Variable button.
    """
    num_exist = kwargs.get("extra_plugins", 0)
    kwargs["extra_plugins"] = num_exist+1

    update_plugin_selections(**kwargs)


def remove_plugin(index, **kwargs ):
    """Remove a variable from the UI.
    
    Remove the entry at the given index and shift all subsequent entries down.
    """
    curr_count = kwargs.get("extra_plugins", 0)
    for i in range(index+1, curr_count+1):
        # Shift all subsequent entries down
        from_parm = kwargs.get("extra_plugin_{}".format(i))
        kwargs["extra_plugin_{}".format(i-1)] = from_parm

    kwargs["extra_plugins"] = curr_count-1
