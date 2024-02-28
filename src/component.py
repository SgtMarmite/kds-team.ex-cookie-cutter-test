"""
Template Component main class.

"""
import logging
from typing import List

from keboola.component.base import ComponentBase, sync_action
from keboola.component.exceptions import UserException
from keboola.component.sync_actions import SelectElement

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = []


class Component(ComponentBase):

    def __init__(self):
        super().__init__()

    def run(self):
        pass

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
