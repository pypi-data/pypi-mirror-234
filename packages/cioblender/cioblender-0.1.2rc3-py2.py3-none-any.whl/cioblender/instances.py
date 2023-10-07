"""Manage instance_type menu."""

from ciocore import data as coredata

def populate_menu(family):
    """Populate instance type menu.

    Get list of items from the shared coredata.
    The menu expects a flat array: [k, v, k,
    v ....]
    """

    if not coredata.valid():
        return [("not_connected", "-- Not Connected --", "")]

    # Todo: implement ensure_valid_selection(node)
    # ensure_valid_selection(node)

    # if connected, get the list of instance types
    instance_data = get_instance_types(family)

    # if there are no instance types, return a default value
    if not instance_data:
        return [("no_instances", "-- No instances --", "")]
    else:
        instance_list = []
        # For each item in the instance_data, add it to the instance_list as a tuple
        for item in instance_data:
            instance_list.append((item["name"], item["description"], ""))
        # Return the instance_list
        return instance_list


def get_instance_types(family="cpu"):
    """Get a list of instance types based on the provided family."""

    family = str(family).lower() if family else "cpu"  # Set default family to "cpu"
    instances = coredata.data()["instance_types"]
    if instances:
        instances = instances.instance_types.values()
        return [item for item in instances if is_family(item, family)]
    else:
        return []



def is_family(item, family):
    return ((family == "gpu") and item.get("gpu")) or ((family == "cpu") and not item.get("gpu"))

# Todo: implement ensure_valid_selection(node)
def ensure_valid_selection(node, **kwargs):
    """
    If connected, ensure the value of this parm is valid.
    """
    if not coredata.valid():
        return

    pass



def resolve_payload(**kwargs):

    instance_type = kwargs.get("machine_type")
    preemptible = kwargs.get("preemptible")
    retries = kwargs.get("preemptible_retries")
    result = {
        "instance_type": instance_type,
        "force": False,
        "preemptible": [False, True][preemptible]
    }

    if retries > 0 and preemptible:
        result["autoretry_policy"] = {"preempted": {"max_retries": retries}}

    return result

