import re
image_regex = re.compile(r"^(?:(?=[^:\/]{1,253})(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*(?::[0-9]{1,5})?/)?((?![._-])(?:[a-z0-9._-]*)(?<![._-])(?:/(?![._-])[a-z0-9._-]*(?<![._-]))*)(?::(?![.-])[a-zA-Z0-9_.-]{1,128})?$")
path_regex = re.compile(r"^([\/]{1}[a-zA-Z0-9.]+)+(\/?){1}$|^([\/]{1})$")
env_name_regex = re.compile(r"^[-._a-zA-Z][-._a-zA-Z0-9]*$")
container_name_regex = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")

def is_valid_env_name(name):
    return env_name_regex.search(name)

def is_valid_container_name(name):
    return container_name_regex.search(name)

def is_image_name(image_name) -> bool:
    return image_regex.search(image_name)

def is_valid_path(path:str) -> bool:
    return path_regex.search(path)

