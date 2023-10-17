import glob
import os
import pathlib
from typing import List, Tuple

from nerdcore.defs import NERDS_PATH
from nerdcore.utils.nerd.theme_functions import print_t, input_t


def list_configs() -> List[str]:
    """ List all nerd configs.
    :return: A list of config names """
    file_paths = glob.glob(os.path.join(NERDS_PATH, '*.yaml'))
    return [os.path.splitext(os.path.basename(file))[0] for file in file_paths]


def get_config_name(given_config_name: str = None, prompt_user: bool = False) -> Tuple[str, str]:
    """ Retrieve the config name and corresponding config path.
    :param prompt_user: Whether the user should be prompted
    :param given_config_name: A given config name
    :return: A tuple consisting of config name and its configuration file path """

    def select_config_from_list() -> str:
        """ Lists all configs and lets user select one.
        :return: Selected config name """

        print_t("Please select from the available configs:", 'warning')
        configs = list_configs()
        for idx, config in enumerate(configs, start=1):
            print_t(f"{idx}. {config}", 'option')
        config_index = int(input_t("Enter the number of the config")) - 1
        return configs[config_index]

    def config_exists(name: str) -> bool:
        """ Checks if a generated nerd config exists.
        :param name: config name
        :return: True if a generated config exists, False otherwise
        """
        return pathlib.Path(os.path.join(NERDS_PATH, f'{name}.yaml')).exists()

    if given_config_name is None:
        if config_exists('default') and not prompt_user:
            print_t(f"No config name provided. Loading default nerd config...", 'config')
            config_name = 'default'
        else:
            config_name = select_config_from_list()
    elif not config_exists(given_config_name):
        print_t("Provided config name does not correspond to an existing configuration. Please select an existing "
                "config:", 'important')
        config_name = select_config_from_list()
    else:
        config_name = given_config_name

    nerd_config_file = os.path.join(NERDS_PATH, f'{config_name}.yaml')
    return config_name, nerd_config_file
