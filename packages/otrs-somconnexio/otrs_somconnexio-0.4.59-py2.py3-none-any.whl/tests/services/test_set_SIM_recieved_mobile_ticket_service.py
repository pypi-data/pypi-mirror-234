import unittest
from datetime import date

from mock import ANY, Mock, call, patch

from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData
from otrs_somconnexio.services.set_SIM_recieved_mobile_ticket import (
    SetSIMRecievedMobileTicket,
)


@patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
@patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.MobileProcessTicket")
@patch("otrs_somconnexio.services.update_ticket_DF.OTRSClient")
class SetSIMRecievedMobileTicketTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_otrs_client = Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        )
        self.mock_mobile_process_ticket = Mock(
            spec=[
                "queue",
                "service_technology",
                "fiber_contract_code",
                "mobile_service_type",
                "confirmed_documentation",
            ]
        )

    def test_run_only_mobile_confirm_doc_no_associated(
        self, MockOTRSClient, MockMobileProcessTicket, MockDF
    ):
        ticket_number = "123"
        MockOTRSClient.return_value = self.mock_otrs_client
        MockMobileProcessTicket.return_value = self.mock_mobile_process_ticket
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid"]
        )
        MockMobileProcessTicket.return_value.confirmed_documentation = "si"
        MockMobileProcessTicket.return_value.fiber_contract_code = False
        MockMobileProcessTicket.return_value.queue = "Serveis mòbil::Provisió mòbil"
        MockMobileProcessTicket.return_value.service_technology = "mòbil"

        SetSIMRecievedMobileTicket(
            ticket_number, date(2023, 1, 20), date(2023, 1, 18)
        ).run()

        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[ANY] * 4,
        )
        MockDF.assert_has_calls(
            [
                call(
                    name="SIMrebuda",
                    value=1,
                ),
                call(
                    name="permetActivacio",
                    value="si",
                ),
                call(name="dataActivacioLiniaMobil", value="2023-01-20"),
                call(name="dataIntroPlataforma", value="2023-01-18"),
            ]
        )

    def test_run_queue_ended_fiber(
        self, MockOTRSClient, MockMobileProcessTicket, MockDF
    ):
        # TODO: Delete this test??
        ticket_number = "123"
        MockOTRSClient.return_value = self.mock_otrs_client
        MockMobileProcessTicket.return_value = self.mock_mobile_process_ticket
        MockDF.return_value = Mock(spec=[])
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid"]
        )
        MockMobileProcessTicket.return_value.queue = (
            "Serveis mòbil::Provisió mòbil::01.1 Fibra finalitzada"  # noqa
        )

        SetSIMRecievedMobileTicket(
            ticket_number, date(2023, 1, 20), date(2023, 1, 18)
        ).run()
        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[ANY] * 4,
        )
        MockDF.assert_has_calls(
            [
                call(
                    name="SIMrebuda",
                    value=1,
                ),
                call(
                    name="permetActivacio",
                    value="si",
                ),
                call(name="dataActivacioLiniaMobil", value="2023-01-20"),
                call(name="dataIntroPlataforma", value="2023-01-18"),
            ]
        )

    def test_run_not_associated_not_portability(
        self, MockOTRSClient, MockMobileProcessTicket, MockDF
    ):
        ticket_number = "123"
        MockMobileProcessTicket.return_value.queue = "Serveis mòbil::Provisió mòbil"
        MockMobileProcessTicket.return_value.mobile_service_type = "altaNova"
        MockMobileProcessTicket.return_value.confirmed_documentation = "si"

        SetSIMRecievedMobileTicket(
            ticket_number,
            date(2023, 1, 20),
            date(2023, 1, 18),
        ).run()

        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[ANY] * 4,
        )
        MockDF.assert_has_calls(
            [
                call(
                    name="SIMrebuda",
                    value=1,
                ),
                call(
                    name="permetActivacio",
                    value="si",
                ),
                call(name="dataActivacioLiniaMobil", value="2023-01-20"),
                call(name="dataIntroPlataforma", value="2023-01-18"),
            ]
        )

    def test_run_only_mobile_no_confirm_doc(
        self, MockOTRSClient, MockMobileProcessTicket, MockDF
    ):
        ticket_number = "123"
        MockMobileProcessTicket.return_value.queue = "Serveis mòbil::Provisió mòbil"
        MockMobileProcessTicket.return_value.mobile_service_type = "altaNova"
        MockMobileProcessTicket.return_value.confirmed_documentation = "no"
        MockMobileProcessTicket.return_value.fiber_contract_code = False

        SetSIMRecievedMobileTicket(
            ticket_number,
            date(2023, 1, 20),
            date(2023, 1, 18),
        ).run()

        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[ANY],
        )
        MockDF.assert_has_calls(
            [
                call(
                    name="SIMrebuda",
                    value=1,
                )
            ]
        )

    def test_run_ticket_not_ready(self, MockMobileProcessTicket, _, __):
        ticket_number = "123"
        MockMobileProcessTicket.return_value.queue = "Serveis mòbil::Provisió BA"

        with self.assertRaises(TicketNotReadyToBeUpdatedWithSIMReceivedData) as error:
            SetSIMRecievedMobileTicket(
                ticket_number, date(2023, 1, 20), date(2023, 1, 18)
            ).run()
            self.assertEqual(
                error.message,
                "Ticket {} not ready to be updated with SIM received data".format(
                    ticket_number
                ),
            )
