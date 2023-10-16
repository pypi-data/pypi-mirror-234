# coding: utf-8
from otrs_somconnexio.client import OTRSClient


class UpdateTicketDF:
    """
    Abstract service class to update a given OTRS ticket DF's.

    Class method '_prepare_dynamic_fields' needs to be implemented in child classes
    """

    def __init__(self, ticket_number):
        self.ticket_number = ticket_number
        self.ticket = None
        self.otrs_client = None

    def _get_ticket(self):
        if not self.otrs_client:
            self.otrs_client = OTRSClient()
        if not self.ticket:
            self.ticket = self.otrs_client.get_ticket_by_number(
                self.ticket_number, dynamic_fields=True
            )

    def run(self):
        self._get_ticket()
        self.otrs_client.update_ticket(
            self.ticket.tid,
            article=None,
            dynamic_fields=self._prepare_dynamic_fields(),
        )
