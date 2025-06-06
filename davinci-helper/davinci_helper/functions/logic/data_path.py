import os, pathlib, importlib

def get_data_directory():
    data_directory = os.getenv("DAVINCI_HELPER_DIR")
    if data_directory and os.path.isdir(data_directory):
        return str(data_directory)
    else:
        return "/usr/share/davinci-helper"

# DEFINING CSS FILES PATH
css_path = os.path.join(get_data_directory(), "data/css")

# DEFINING UI FILES PATH
ui_path = os.path.join(get_data_directory(), "data/ui")

# DEFINING ICON FILES PATH
icon_path = os.path.join(get_data_directory(), "data/icons")

# DEFINING TRANSLATE FILES PATH
locale_path = os.path.join(get_data_directory(), "locale")

# DEFINING SETTINGS FILES PATH
home_dir = os.path.expanduser("~")
settings_path = os.path.join(home_dir, ".config/davinci_helper")


def _find_package_dir() -> str:
    """
    1) If DAVINCI_HELPER_DIR is set, assume we run from the source tree and
       return <DIR>/davinci_helper.
    2) Otherwise locate the 'davinci_helper' package and return its directory,
       e.g. /usr/lib/python3.12/site-packages/davinci_helper
       or ~/.local/lib/python3.12/site-packages/davinci_helper.
    """
    dev_root = os.getenv("DAVINCI_HELPER_DIR")
    if dev_root:
        candidate = pathlib.Path(dev_root) / "davinci_helper"
        if candidate.is_dir():
            return str(candidate)

    spec = importlib.util.find_spec("davinci_helper")
    if spec and spec.origin:
        return str(pathlib.Path(spec.origin).parent)

    # Fallback – should never happen unless the package is broken
    return "/usr/lib/python3/site-packages/davinci_helper"

PACKAGE_PATH = _find_package_dir()