import dataclasses
import os
import re
from dataclasses import dataclass

from nerdcore.config.yaml_helpers import get_nerd_config_defaults
from nerdcore.defs import NERDS_PATH, import_env_class
from nerdcore.utils.nerd.theme_functions import print_t
from nerdcore.utils.nerd_config.nerd_config_validations import is_prompt_key

ENV = import_env_class()


def insert_cop_file_contents(value: str) -> str:
    matches = re.findall(r'{cop:(.*?)}', value)
    for match in matches:
        expanded_path = os.path.expanduser(match)
        if os.path.isfile(expanded_path):
            with open(expanded_path, "r") as file:
                file_content = file.read()
            value = value.replace(f'{{cop:{match}}}', file_content)
        else:
            raise FileNotFoundError(f"Could not find the file specified in the 'cop' placeholder: {expanded_path}")
    return value


@dataclass
class NerdConfig:
    _instance = None

    """ NERD_CONFIG_PROPS - DO NOT MODIFY
        Definitions of NerdConfig props, generated from nerd-config-defaults. """
    # [NERD_CONFIG_PROPS_START]
    from typing import Optional

    from ruamel.yaml.scalarfloat import ScalarFloat
    from dataclasses import field
    DEPLOY_TYPE: Optional[str] = field(default=None)
    COMPOSER_INSTALL: Optional[bool] = field(default=None)
    BACKUP_DB: Optional[bool] = field(default=None)
    RUN_MIGRATIONS: Optional[bool] = field(default=None)
    REBUILD_STACKABLE_CACHES: Optional[bool] = field(default=None)
    BUILD_NPM: Optional[None] = field(default=None)
    SMOKE_TEST_FILE_PATH: Optional[str] = field(default=None)
    # [NERD_CONFIG_PROPS_END]

    env: Optional[ENV] = field(default=None)

    def __post_init__(self):
        # print_t(f"Loaded NerdConfig: {self.__dict__}", 'info')

        """ NERD_CONFIG_VALIDATIONS - DO NOT MODIFY
        Set NerdConfig props with validations, generated from nerd-config-defaults & nerd_config_validations. """
        # [NERD_CONFIG_VALIDATIONS_START]
        from nerdcore.utils.nerd_config.nerd_config_validations import validate_str, validate_bool, validate_int, validate_float, validate_path, validate_list_str
        self.DEPLOY_TYPE = validate_str('DEPLOY_TYPE', self.DEPLOY_TYPE)
        self.COMPOSER_INSTALL = validate_bool('COMPOSER_INSTALL', self.COMPOSER_INSTALL)
        self.BACKUP_DB = validate_bool('BACKUP_DB', self.BACKUP_DB)
        self.RUN_MIGRATIONS = validate_bool('RUN_MIGRATIONS', self.RUN_MIGRATIONS)
        self.REBUILD_STACKABLE_CACHES = validate_bool('REBUILD_STACKABLE_CACHES', self.REBUILD_STACKABLE_CACHES)
        self.SMOKE_TEST_FILE_PATH = validate_path('SMOKE_TEST_FILE_PATH', self.SMOKE_TEST_FILE_PATH)
        # [NERD_CONFIG_VALIDATIONS_END]

        self.env = ENV.get()

    @classmethod
    def load(cls, config_name: str) -> 'NerdConfig':
        from nerdcore.config.yaml_helpers import read_yaml_file

        if cls._instance is None:
            config_path = os.path.join(NERDS_PATH, f"{config_name}.yaml")

            if not os.path.exists(config_path):
                raise FileNotFoundError(f"nerd-manifest.yaml configuration file {config_path} not found.")

            config_dict = read_yaml_file(config_path, ruamel=True)
            config_dict = cls.filter_config_values(config_dict)
            config_dict = cls.apply_defaults(config_dict)

            cls._instance = NerdConfig(**config_dict)

        return cls._instance

    @classmethod
    def apply_default_and_validate(cls, data: dict):
        """
        Validate the provided dictionary with NerdConfig and return it.
        """

        data = cls.filter_config_values(data)
        data = cls.apply_defaults(data)

        # Create an instance of NerdConfig to perform validation
        try:
            validated_config = cls(**data)
        except (TypeError, ValueError) as e:
            print_t(f"NerdConfig Validation - {e}", 'error')
            exit()

        data = validated_config.__dict__
        data.pop('env', None)

        return data

    @classmethod
    def filter_config_values(cls, config_values: dict) -> dict:
        # Get dictionary of NerdConfig properties
        config_properties = {f.name for f in dataclasses.fields(cls)}
        config_properties.remove('env')

        # Remove any keys from data that aren't properties of the NerdConfig class
        config_values = {k: v for k, v in config_values.items() if k in config_properties}

        return config_values

    @classmethod
    def apply_defaults(cls, config_values: dict) -> dict:
        """
        Apply default values to the provided dictionary with NerdConfig and return it.
        If a value is set to None, it will be maintained as None.
        If a value isn't present, it will be set to the default value.
        :param config_values: dict
        :return: dict
        """

        # Get dictionary of NerdConfig properties so we don't default to env vars that aren't properties
        config_properties = {f.name for f in dataclasses.fields(cls)}
        config_properties.remove('env')

        nerd_config_defaults = get_nerd_config_defaults()
        for attribute in nerd_config_defaults:
            if config_values.get(attribute, '**unset') == '**unset' and nerd_config_defaults[attribute] is not None:
                config_values[attribute] = nerd_config_defaults[attribute]

        return config_values

    def replace_prompt_str(self, to_replace, replace_with):
        copy = NerdConfig(**self.__dict__)
        for attr in vars(copy):
            value = getattr(copy, attr)
            if is_prompt_key(attr) and value is not None:
                setattr(copy, attr, value.replace(to_replace, replace_with))
        return copy
