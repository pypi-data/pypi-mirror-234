from pyotrs.lib import DynamicField

from otrs_somconnexio.otrs_models.configurations.changes.change_shared_bond import (
    ChangeSharedBondTicketConfiguration,
)

from .base_customer_ticket import BaseCustomerTicket


class ChangeSharedBondTicket(BaseCustomerTicket):
    def __init__(
        self,
        username,
        customer_code,
        fields_dict,
        override_ticket_ids=[],
        fallback_path="/tmp/tickets/",
    ):
        super(ChangeSharedBondTicket, self).__init__(
            username, customer_code, fields_dict, override_ticket_ids, fallback_path
        )
        self.configuration = ChangeSharedBondTicketConfiguration()

    def get_search_args(self):
        return {
            "dynamic_fields": [
                DynamicField(
                    "ProcessManagementProcessID", self.configuration.process_id
                ),
                DynamicField(
                    "ProcessManagementActivityID", self.configuration.activity_id
                ),
            ],
            "Queues": [self.configuration.queue],
            "States": [self.configuration.state],
        }

    def _get_subject(self):
        return "Sol·licitud Canvi d'abonament compartit oficina virtual"

    def _get_queue(self):
        return self.configuration.queue

    def _get_dynamic_fields(self):
        return {
            "liniaMobil": self.fields["phone_number"],
            "productMobil": self.fields["new_product_code"],
            "IDAbonamentCompartit": self.fields["new_shared_bond"],
            "OdooContractRefRelacionat": self.fields["fiber_linked"],
        }
