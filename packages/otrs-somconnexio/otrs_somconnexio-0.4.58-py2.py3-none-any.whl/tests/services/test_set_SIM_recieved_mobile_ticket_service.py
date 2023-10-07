import unittest
from datetime import date

from mock import ANY, Mock, call, patch

from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData
from otrs_somconnexio.services.set_SIM_recieved_mobile_ticket import (
    SetSIMRecievedMobileTicket,
)


class SetSIMRecievedMobileTicketTestCase(unittest.TestCase):
    @patch(
        "otrs_somconnexio.services.update_ticket_DF.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_only_mobile_confirm_doc(self, MockDF, MockOTRSClient):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.dynamic_field_get.return_value.value = (
            "si"  # noqa
        )

        def field_get_side_effect(key):
            if key == "Queue":
                return "Serveis mòbil::Provisió mòbil"

        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.side_effect = (
            field_get_side_effect
        )

        SetSIMRecievedMobileTicket(
            ticket_number, True, ANY, ANY, date(2023, 1, 20), date(2023, 1, 18)
        ).run()

        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df] * 4,
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

    @patch(
        "otrs_somconnexio.services.update_ticket_DF.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_only_mobile_no_confirm_doc(self, MockDF, MockOTRSClient):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = (
            "XXX"
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.dynamic_field_get.return_value.value = (
            "no"  # noqa
        )

        SetSIMRecievedMobileTicket(
            ticket_number, True, ANY, ANY, ANY, date(2023, 1, 20), date(2023, 1, 18)
        ).run()

        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df],
        )
        MockDF.assert_has_calls(
            [
                call(
                    name="SIMrebuda",
                    value=1,
                )
            ]
        )

    @patch(
        "otrs_somconnexio.services.update_ticket_DF.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_ended_fiber(self, MockDF, MockOTRSClient):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = (
            "Serveis mòbil::Provisió mòbil::01.1 Fibra finalitzada"  # noqa
        )
        SetSIMRecievedMobileTicket(
            ticket_number, ANY, ANY, ANY, date(2023, 1, 20), date(2023, 1, 18)
        ).run()
        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df] * 4,
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

    @patch(
        "otrs_somconnexio.services.update_ticket_DF.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_not_associated_not_portability(self, MockDF, MockOTRSClient):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.dynamic_field_get.return_value.value = (
            "si"  # noqa
        )

        def field_get_side_effect(key):
            if key == "Queue":
                return "Serveis mòbil::Provisió mòbil"

        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.side_effect = (
            field_get_side_effect
        )
        only_mobile = False
        associated = False
        portability = False

        SetSIMRecievedMobileTicket(
            ticket_number,
            only_mobile,
            associated,
            portability,
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
            dynamic_fields=[expected_df] * 4,
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

    @patch(
        "otrs_somconnexio.services.update_ticket_DF.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_only_mobile_no_confirm_doc(self, MockDF, MockOTRSClient):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = (
            "XXX"
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.dynamic_field_get.return_value.value = (
            "no"  # noqa
        )

        def field_get_side_effect(key):
            if key == "Queue":
                return "Serveis mòbil::Provisió mòbil"

        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.side_effect = (
            field_get_side_effect
        )
        only_mobile = False
        associated = True
        portability = False

        SetSIMRecievedMobileTicket(
            ticket_number,
            only_mobile,
            associated,
            portability,
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
            dynamic_fields=[expected_df],
        )
        MockDF.assert_has_calls(
            [
                call(
                    name="SIMrebuda",
                    value=1,
                )
            ]
        )

    @patch(
        "otrs_somconnexio.services.update_ticket_DF.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket",
                "get_ticket_by_number",
            ]
        ),
    )
    def test_run_only_mobile_no_confirm_doc(self, MockOTRSClient):
        ticket_number = "123"
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get"]
        )

        def field_get_side_effect(key):
            if key == "Queue":
                return "Serveis mòbil::Provisió BA"

        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.side_effect = (
            field_get_side_effect
        )

        with self.assertRaises(TicketNotReadyToBeUpdatedWithSIMReceivedData) as error:
            SetSIMRecievedMobileTicket(
                ticket_number, ANY, ANY, ANY, date(2023, 1, 20), date(2023, 1, 18)
            ).run()
            self.assertEqual(
                error.message,
                "Ticket {} not ready to be updated with SIM received data".format(
                    ticket_number
                ),
            )
