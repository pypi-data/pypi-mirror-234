

def resolve_payload(**kwargs):
    output_folder = kwargs.get("output_folder").strip()
    output_folder = output_folder.replace("\\", "/")
    return {"output_path": output_folder}