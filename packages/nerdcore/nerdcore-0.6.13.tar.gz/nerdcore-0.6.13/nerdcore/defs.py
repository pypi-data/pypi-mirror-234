import os

from nerdcore.utils.ncdefs_utils import find_project_root, import_class_from_path_with_fallback
from nerdcore.utils.ncdefs_utils import get_python_command

"""  PREDEFINED FRAMEWORK INSTANCE PATHS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """

# ROOT_PATH
ROOT_PATH = find_project_root()

# DEPLOYMENTS
DEPLOYMENTS_PATH = os.path.join(ROOT_PATH, "deployments")
# TASKS
TASKS_PATH = os.path.join(ROOT_PATH, "tasks")
# ABILITIES
ABILITIES_PATH = os.path.join(ROOT_PATH, "abilities")
# COMMANDS
COMMANDS_PATH = os.path.join(ROOT_PATH, "commands")

# ENV
ENV_PATH = os.path.join(ROOT_PATH, ".env")
# CONFIG
CONFIG_PATH = os.path.join(ROOT_PATH, "config")
# NERD MANIFEST
NERD_MANIFEST_PATH = os.path.join(CONFIG_PATH, 'nerd-manifest.yaml')
# NERD CONFIG DEFAULTS
NERD_CONFIG_DEFAULTS_PATH = os.path.join(CONFIG_PATH, 'nerd-config-defaults.yaml')

# FRAMEWORK CONFIG
FRAMEWORK_CONFIG_PATH = os.path.join(CONFIG_PATH, 'framework')
# THEME CONFIG
THEME_CONFIG_PATH = os.path.join(FRAMEWORK_CONFIG_PATH, 'theme.py')
# ENV CLASS
ENV_CLASS_PATH = os.path.join(FRAMEWORK_CONFIG_PATH, "env_class.py")
# NERD CONFIG CLASS
NERD_CONFIG_CLASS_PATH = os.path.join(FRAMEWORK_CONFIG_PATH, "nerd_config_class.py")

# STOR
STOR_PATH = os.path.join(ROOT_PATH, "stor")
# TEMP
TEMP_PATH = os.path.join(STOR_PATH, "temp")

# NERD TEMP CONFIG FILES
NERDS_PATH = os.path.join(TEMP_PATH, 'nerds')

"""  'GLOBAL' HELPERS/VARIABLES
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """
#
# ENABLE_RELATIVE_IMPORTS = sys.path.append(ROOT_PATH)

# GET user's available Python command
PYTHON_COMMAND = get_python_command()

TOKEN_UNCERTAINTY_BUFFER = 10

# OS-agnostic newline characters
nl = os.linesep
nl2 = nl * 2


def or_(lambda_access_attempt, default=None):
    try:
        return lambda_access_attempt()
    except (AttributeError, NameError):
        return default


def import_nerd_config_class():
    from nerdcore.config.nerd_config_class import NerdConfig as DefaultNerdConfigClass
    return import_class_from_path_with_fallback(NERD_CONFIG_CLASS_PATH, 'NerdConfig', DefaultNerdConfigClass)


def import_env_class():
    from nerdcore.config.env_class import ENV as DEFAULT_ENV_CLASS
    return import_class_from_path_with_fallback(ENV_CLASS_PATH, 'ENV', DEFAULT_ENV_CLASS)
