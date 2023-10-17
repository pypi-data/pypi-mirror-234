import os

from nerdcore.defs import import_nerd_config_class, TEMP_PATH
from nerdcore.utils.nerd.get_config_name import get_config_name
from nerdcore.utils.nerd.theme_functions import print_t, input_t, apply_t

NerdConfig = import_nerd_config_class()


def set_loaded_config(given_config_name: str) -> None:
    loaded_config_path = os.path.join(TEMP_PATH, "loaded-config-name.txt")
    with open(loaded_config_path, 'w') as file:
        file.write(given_config_name)


def get_loaded_config() -> str or None:
    loaded_nerd_config_path = os.path.join(TEMP_PATH, "loaded-config-name.txt")
    if not os.path.exists(loaded_nerd_config_path):
        return None
    with open(loaded_nerd_config_path, 'r') as file:
        config_name = file.read()
    if config_name == '':
        return None
    return config_name


def load_nerd_config(given_config_name=None) -> (NerdConfig, str):
    loaded_config_name = get_loaded_config()
    if loaded_config_name is not None and given_config_name is None:
        use_current = input_t(f"Continue with loaded config: {apply_t(loaded_config_name, 'important')}?", '(y/n)')
        if use_current == 'y':
            config_name = loaded_config_name
        else:
            config_name, _ = get_config_name(prompt_user=True)
    elif given_config_name is not None:
        config_name = given_config_name
    else:
        print_t("No config name or currently loaded config.", "quiet")
        config_name, _ = get_config_name(prompt_user=True)

    set_loaded_config(config_name)
    return NerdConfig.load(config_name=config_name), config_name
