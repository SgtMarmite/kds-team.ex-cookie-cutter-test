"""
Template Component main class.

"""
import csv
import logging
from datetime import datetime
from typing import List

from keboola.component.base import ComponentBase, sync_action
from keboola.component.exceptions import UserException
from keboola.component.sync_actions import SelectElement


# configuration variables
KEY_API_TOKEN = '#api_token'
KEY_PRINT_HELLO = 'print_hello'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_PRINT_HELLO]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Main execution code
        """

        # ####### EXAMPLE TO REMOVE
        # check for missing configuration parameters
        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        self.validate_image_parameters(REQUIRED_IMAGE_PARS)
        params = self.configuration.parameters
        # Access parameters in data/config.json
        if params.get(KEY_PRINT_HELLO):
            logging.info("Hello Worldd")

        # get input table definitions
        input_tables = self.get_input_tables_definitions()
        for table in input_tables:
            logging.info(f'Received input table: {table.name} with path: {table.full_path}')

        if len(input_tables) == 0:
            raise UserException("No input tables found")

        # get last state data/in/state.json from previous run
        previous_state = self.get_state_file()
        logging.info(previous_state.get('some_state_parameter'))

        # Create output table (Tabledefinition - just metadata)
        table = self.create_out_table_definition('output.csv', incremental=True, primary_key=['timestamp'])

        # get file path of the table (data/out/tables/Features.csv)
        out_table_path = table.full_path
        logging.info(out_table_path)

        # Add timestamp column and save into out_table_path
        input_table = input_tables[0]
        with (open(input_table.full_path, 'r') as inp_file,
              open(table.full_path, mode='wt', encoding='utf-8', newline='') as out_file):
            reader = csv.DictReader(inp_file)

            columns = list(reader.fieldnames)
            # append timestamp
            columns.append('timestamp')

            # write result with column added
            writer = csv.DictWriter(out_file, fieldnames=columns)
            writer.writeheader()
            for in_row in reader:
                in_row['timestamp'] = datetime.now().isoformat()
                writer.writerow(in_row)

        # Save table manifest (output.csv.manifest) from the tabledefinition
        self.write_manifest(table)

        # Write new state - will be available next run
        self.write_state_file({"some_state_parameter": "value"})

        # ####### EXAMPLE TO REMOVE END

    @sync_action("listEndpoints")
    def list_modules(self) -> List[SelectElement]:
        endpoints = ["endpoint1", "endpoint2", "endpoint3", "endpoint4", "endpoint5"]
        return [SelectElement(label=endpoint, value=endpoint) for endpoint in endpoints]

    @sync_action("listFields")
    def list_fields(self) -> List[SelectElement]:
        fields = ["field1", "field2", "field3", "field4", "field5", "field6", "field7", "field8", "field9"]
        fieldnames = ["Field1", "Field2", "Field3", "Field4", "Field5", "Field6", "Field7", "Field8", "Field9"]
        return [SelectElement(label=name, value=field) for field, name in zip(fields, fieldnames)]


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
