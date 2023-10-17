import os
import shutil

from nerdcore.base_entities.command_class import Command
from nerdcore.defs import COMMANDS_PATH, DEPLOYMENTS_PATH
from nerdcore.ncdefs import NC_EXAMPLE_COMMAND_PATH, NC_EXAMPLE_DEPLOYMENT_PATH


class Make(Command):
    # Specify args that are required (must be initialized as None)
    required_arg_keys = ['entity_type', 'entity_name']

    # Specify unnamed args (passed without --name) (define in passing order)
    unnamed_arg_keys = ['entity_type', 'entity_name']

    # Define and set defaults for all args (incl required)
    # Setting type-hints will provide validation in CliRunnable base class.
    entity_type: str = None
    entity_name: str = None

    ENTITY_TYPE_INFO = {
        'command': (COMMANDS_PATH, NC_EXAMPLE_COMMAND_PATH, 'ExampleCommand'),
        'deployment': (DEPLOYMENTS_PATH, NC_EXAMPLE_DEPLOYMENT_PATH, 'ExampleDeployment'),
    }

    def run(self):

        if not self.entity_name.replace('-', '').isalpha():
            raise ValueError(f"Invalid name: {self.entity_name}. Please specify in kebab-case (e.g. entity-name).")

        # Get info based on the entity type
        entity_path, example_path, example_name = self.ENTITY_TYPE_INFO.get(self.entity_type)

        new_entity_path = os.path.join(entity_path, f'{self.entity_name}.py')
        shutil.copy(example_path, new_entity_path)

        with open(new_entity_path, 'r') as f:
            file_contents = f.read()

        file_contents = file_contents.replace(example_name, self.entity_name.title().replace('-', ''))

        with open(new_entity_path, 'w') as f:
            f.write(file_contents)
