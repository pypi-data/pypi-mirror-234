import os

from pkg_resources import resource_filename

VERSION = '0.6.13'

"""  CORE PATHS

This is a framework-level PATH definitions file.
It is separate from defs.py for usage in nerd-new, when there is no project ROOT_PATH.
It is also used anywhere else a framework-level path is needed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """

# NC PATH (root package)
NC_PATH = os.path.dirname(__file__)

# CM DEPLOYMENTS
NC_DEPLOYMENTS_PATH = resource_filename('nerdcore', "deployments")
# CM TASKS
NC_TASKS_PATH = resource_filename('nerdcore', "tasks")
# CM ABILITIES
NC_ABILITIES_PATH = resource_filename('nerdcore', "abilities")
# CM COMMANDS
NC_COMMANDS_PATH = resource_filename('nerdcore', "commands")
# CM CONFIG
NC_CONFIG_PATH = resource_filename('nerdcore', "config")

# ENV CLASS
NC_ENV_CLASS_PATH = os.path.join(NC_CONFIG_PATH, "env_class.py")
# NERD CONFIG CLASS
NC_NERD_CONFIG_CLASS_PATH = os.path.join(NC_CONFIG_PATH, "nerd_config_class.py")
# THEME CONFIG
NC_THEME_CONFIG_PATH = os.path.join(NC_CONFIG_PATH, 'theme.py')

# HELP
NC_HELP_PATH = resource_filename('nerdcore', "help")

# STOR CORE
NC_STOR_PATH = resource_filename('nerdcore', "stor")
NC_STOR_TEMP_PATH = os.path.join(NC_STOR_PATH, "temp")
NC_STOR_NERD_PATH = os.path.join(NC_STOR_PATH, "nerd")
NC_STOR_SNIPPETS_PATH = os.path.join(NC_STOR_PATH, 'snippets')
NC_STOR_DEFAULTS_PATH = os.path.join(NC_STOR_PATH, "defaults")

# DEFAULTS
NC_ENV_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, ".env.default")
NC_NERD_MANIFEST_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, "nerd-manifest.yaml")
NC_NERD_CONFIG_DEFAULTS_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, "nerd-config-defaults.yaml")
NC_GITIGNORE_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, '.default-gitignore')
NC_REQUIREMENTS_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, 'default-requirements.txt')
NC_README_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, 'DEFAULT-README.md')
NC_APPS_CONFIG_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, 'apps.py')

# ENTITY EXAMPLES
NC_ENTITY_EXAMPLES_PATH = os.path.join(NC_STOR_PATH, "entity_examples")
NC_EXAMPLE_COMMAND_PATH = os.path.join(NC_ENTITY_EXAMPLES_PATH, "example-command.py")
NC_EXAMPLE_DEPLOYMENT_PATH = os.path.join(NC_ENTITY_EXAMPLES_PATH, "example-deployment.py")
