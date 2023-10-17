from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

from pytest_ansible.host_manager import BaseHostManager
from pytest_ansible.module_dispatcher.v28 import ModuleDispatcherV28


class HostManagerV28(BaseHostManager):
    """Fixme."""

    def __init__(self, *args, **kwargs) -> None:
        """Fixme."""
        super().__init__(*args, **kwargs)
        self._dispatcher = ModuleDispatcherV28

    def initialize_inventory(self):
        self.options["loader"] = DataLoader()
        self.options["inventory_manager"] = InventoryManager(
            loader=self.options["loader"],
            sources=self.options["inventory"],
        )
        self.options["variable_manager"] = VariableManager(
            loader=self.options["loader"],
            inventory=self.options["inventory_manager"],
        )
