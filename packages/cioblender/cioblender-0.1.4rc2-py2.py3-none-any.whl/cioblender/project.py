"""Manage project menu selection."""


from ciocore import data as coredata


def populate_menu(node):
    """Populate project menu.

    Get list of items from the shared data_block where they
    have been cached. The menu needs a list: [(p, p, ""), ....]

    Since projects are simply a list of names, the k and v can be the same.
    """

    # if not connected, return a default value

    if not coredata.valid():
        return [("not_connected", "-- Not Connected --", "")]
    # if connected, ensure the value of this parm is valid.

    # Todo: implement ensure_valid_selection(node)
    # ensure_valid_selection(node)

    # if connected, get the list of projects
    project_data = coredata.data()["projects"]

    # if there are no projects, return a default value
    if not project_data:
        return [("no_projects", "-- No Projects --", "")]
    else:
        # Create a dictionary of projects
        blender_projects = {}
        # For each project in the project_data, if the project is not in the blender_projects dictionary,
        # add it to the dictionary
        for project in project_data:
            if project not in blender_projects:
                blender_projects[project] = (project, project, "")
        # Return the list of projects in reverse order, as Blender sorts the list in reverse order
        return list(blender_projects.values())[::-1]


def ensure_valid_selection(node):
    # Todo: implement ensure_valid_selection(node)
    pass

def resolve_payload(**kwargs):
    return {"project": kwargs.get("project")}
