import json



from cioblender import (
    job_title,
    project,
    instances,
    software,
    environment,
    driver,
    frames,
    task,
    assets,
    miscellaneous,
)



def set_stats_panel(**kwargs):
    """Update the stats panel.

    Currently, only gets frames info, but will probably get other (non-payload) info like cost
    estimate. Example, when chunk size of frames change value.
    """
    #frames.set_stats_panel(**kwargs)
    pass


def resolve_payload(**kwargs):
    #set_stats_panel(**kwargs)

    payload = {}
    payload.update(job_title.resolve_payload(**kwargs))
    payload.update(project.resolve_payload(**kwargs))
    payload.update(software.resolve_payload(**kwargs))
    payload.update(miscellaneous.resolve_payload(**kwargs))
    payload.update(instances.resolve_payload(**kwargs))
    payload.update(driver.resolve_payload(**kwargs))
    payload.update(environment.resolve_payload(**kwargs))
    payload.update(assets.resolve_payload(**kwargs))
    payload.update(frames.resolve_payload(**kwargs))
    payload.update(task.resolve_payload(**kwargs))

    return payload
