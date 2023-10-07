""" Module for job title resolver"""


def resolve_payload(**kwargs):
    title = kwargs.get("job_title").strip()
    return {"job_title": title}
