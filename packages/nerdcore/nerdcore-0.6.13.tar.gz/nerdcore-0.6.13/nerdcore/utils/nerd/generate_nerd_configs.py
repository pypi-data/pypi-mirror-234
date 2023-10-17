import os
import shutil
import time

from nerdcore.config.yaml_helpers import read_yaml_file, write_yaml_file
from nerdcore.defs import NERDS_PATH, NERD_MANIFEST_PATH
from nerdcore.defs import import_nerd_config_class
from nerdcore.utils.nerd.theme_functions import print_t

NerdConfig = import_nerd_config_class()


def generate_nerd_configs():

    os.makedirs(os.path.join(NERDS_PATH), exist_ok=True)

    try:
        manifest_nerd_configs = read_yaml_file(NERD_MANIFEST_PATH)
    except FileNotFoundError:
        print_t(f"Could not find nerd-manifest.yaml file. File expected to exist at {NERD_MANIFEST_PATH}", 'error')
        return

    # Create the directories and config files
    for config_name, manifest_config in manifest_nerd_configs.items():
        merged_config = NerdConfig.apply_default_and_validate(manifest_config)

        # Check if new config content is different from the existing one
        generated_config_path = os.path.join(NERDS_PATH, f'{config_name}.yaml')
        if os.path.exists(generated_config_path):
            existing_config = read_yaml_file(generated_config_path)
            if existing_config == merged_config:
                continue
            else:
                os.makedirs(os.path.join(NERDS_PATH, '.history', config_name), exist_ok=True)
                timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
                shutil.move(generated_config_path, os.path.join(NERDS_PATH, '.history', config_name, f'{timestamp}.yaml'))
                # Write to the file
                write_yaml_file(generated_config_path, merged_config, ruamel=True)
        else:
            write_yaml_file(generated_config_path, merged_config, ruamel=True)

    # Remove any nerd configs that are no longer in the manifest
    for config_name in os.listdir(NERDS_PATH):
        if config_name.endswith('.yaml'):
            config_name = config_name[:-5]
            if config_name not in manifest_nerd_configs:
                os.makedirs(os.path.join(NERDS_PATH, '.history', config_name), exist_ok=True)
                timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
                removed_config_path = os.path.join(NERDS_PATH, f'{config_name}.yaml')
                shutil.move(removed_config_path,
                            os.path.join(NERDS_PATH, '.history', config_name, f'{timestamp}.yaml'))
                os.remove(os.path.join(NERDS_PATH, f'{config_name}.yaml'))
