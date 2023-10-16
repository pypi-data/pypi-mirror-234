import json
import os
import uuid

from pyotrs import Ticket, Article
from pyotrs.lib import DynamicField

from otrs_somconnexio.client import OTRSClient


class BaseTicket:
    def __init__(
        self,
        username,
        customer_code,
        fields_dict,
        override_ticket_ids=[],
        fallback_path="/tmp/tickets/",
    ):
        self.username = username
        self.customer_code = customer_code
        self.fields = fields_dict
        self.client = None
        self.override_ticket_ids = override_ticket_ids
        self.fallback_path = fallback_path

    def _get_subject(self):
        raise NotImplementedError("Tickets must implement _get_subject")

    def _get_body(self):
        return "-"

    def _get_state(self):
        return "new"

    def _get_priority(self):
        return "3 normal"

    def _get_queue(self):
        raise NotImplementedError("Tickets must implement _get_queue")

    def _get_dynamic_fields(self):
        raise NotImplementedError("Tickets must implement _get_dynamic_fields")

    def _dict_to_dynamic_fields(self, d):
        return [DynamicField(key, d[key]) for key in d if d[key]]

    def send_ticket(self):
        subject = self._get_subject()
        body = self._get_body()
        queue = self._get_queue()

        article = Article({"Subject": subject, "Body": body})
        new_ticket = Ticket(
            {
                "Title": subject,
                "Queue": queue,
                "State": self._get_state(),
                "Type": self._get_type(),
                "Priority": self._get_priority(),
                "CustomerUser": self.customer_code,
                "CustomerID": self.customer_code,
            }
        )

        dynamic_fields = self._dict_to_dynamic_fields(
            self._get_process_management_dynamic_fields()
        ) + self._dict_to_dynamic_fields(self._get_dynamic_fields())

        return self._client().create_otrs_process_ticket(
            new_ticket,
            article=article,
            dynamic_fields=dynamic_fields,
        )

    def _transform_boolean_df(self, boolean):
        # Transform boolean DF into '0'/'1' value
        return "1" if bool(boolean) else "0"

    def store_ticket(self):
        ticket_path = os.path.join(self.fallback_path, str(uuid.uuid4()) + ".json")

        # ensure ticket fallback path exists
        if not os.path.exists(self.fallback_path):
            os.makedirs(self.fallback_path)

        with open(ticket_path, "w") as f:
            json.dump({"customer_code": self.customer_code, "fields": self.fields}, f)

    def create(self):
        return self.send_ticket()

    def get(self, idov):
        """Get a ticket searching by IDOV DynamicField."""
        ticket = self._client().client.ticket_search(
            dynamic_fields=[DynamicField("IDOV", search_patterns=idov)]
        )
        if ticket:
            return self._client().client.ticket_get_by_id(ticket_id=ticket[0])

    def update(self, ticket_id, article=None, dynamic_fields=None):
        self._client().client.ticket_update(
            ticket_id,
            article=article,
            dynamic_fields=dynamic_fields,
        )

    def _client(self):
        if self.client:
            return self.client

        self.client = OTRSClient()

        return self.client
