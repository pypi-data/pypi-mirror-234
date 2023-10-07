from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket import (
    ChangeTariffTicket,
    ChangeTariffExceptionalTicket,
)
from otrs_somconnexio.otrs_models.configurations.changes.change_tariff import (
    ChangeTariffTicketConfiguration,
    ChangeTariffExceptionalTicketConfiguration,
)


class TestCaseChangeTariffTicket:
    def test_create(self, mocker):
        username = "7456787G"
        customer_code = "1234"

        OTRSClientMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient",
            return_value=mocker.Mock(),
        )
        OTRSClientMock.return_value.create_otrs_process_ticket.return_value = (
            mocker.Mock(spec=["id"])
        )
        OTRSClientMock.return_value.create_otrs_process_ticket.return_value.id = "1"

        TicketMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket",
            return_value=mocker.Mock(),
        )
        ArticleMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article",
            return_value=mocker.Mock(),
        )
        DynamicFieldMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField",
            return_value=mocker.Mock(),
        )

        expected_ticket_data = {
            "Title": "Sol·licitud Canvi de tarifa oficina virtual",
            "Queue": ChangeTariffTicketConfiguration.queue,
            "State": ChangeTariffTicketConfiguration.state,
            "Type": ChangeTariffTicketConfiguration.type,
            "Priority": ChangeTariffTicketConfiguration.priority,
            "CustomerUser": customer_code,
            "CustomerID": customer_code,
        }
        expected_article_data = {
            "Subject": "Sol·licitud Canvi de tarifa oficina virtual",
            "Body": "-",
        }

        fields_dict = {
            "phone_number": "666666666",
            "new_product_code": "NEW_PRODUCT_CODE",
            "current_product_code": "CURRENT_PRODUCT_CODE",
            "effective_date": "tomorrow",
            "fiber_linked": "",
            "subscription_email": "fakeemail@email.coop",
            "language": "ca_ES",
            "send_notification": False,
        }

        ticket = ChangeTariffTicket(username, customer_code, fields_dict).create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        calls = [
            mocker.call(
                "ProcessManagementProcessID", ChangeTariffTicketConfiguration.process_id
            ),
            mocker.call(
                "ProcessManagementActivityID",
                ChangeTariffTicketConfiguration.activity_id,
            ),
            mocker.call("renovaCanviTarifa", "0"),
            mocker.call("liniaMobil", "666666666"),
            mocker.call("productMobil", "NEW_PRODUCT_CODE"),
            mocker.call("tarifaAntiga", "CURRENT_PRODUCT_CODE"),
            mocker.call("dataExecucioCanviTarifa", "tomorrow"),
            mocker.call("correuElectronic", "fakeemail@email.coop"),
            mocker.call("idioma", "ca_ES"),
            mocker.call("enviarNotificacio", "0"),
        ]
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.create_otrs_process_ticket.assert_called_once_with(  # noqa
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls],
        )
        assert ticket.id == "1"

    def test_create_with_override_tickets(self, mocker):
        username = "7456787G"
        customer_code = "1234"

        OTRSClientMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient",
            return_value=mocker.Mock(),
        )
        TicketMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket",
            return_value=mocker.Mock(),
        )
        ArticleMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article",
            return_value=mocker.Mock(),
        )
        DynamicFieldMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField",
            return_value=mocker.Mock(),
        )

        expected_ticket_data = {
            "Title": "Sol·licitud Canvi de tarifa oficina virtual",
            "Queue": ChangeTariffTicketConfiguration.queue,
            "State": ChangeTariffTicketConfiguration.state,
            "Type": ChangeTariffTicketConfiguration.type,
            "Priority": ChangeTariffTicketConfiguration.priority,
            "CustomerUser": customer_code,
            "CustomerID": customer_code,
        }
        expected_article_data = {
            "Subject": "Sol·licitud Canvi de tarifa oficina virtual",
            "Body": "-",
        }

        fields_dict = {
            "phone_number": "666666666",
            "new_product_code": "NEW_PRODUCT_CODE",
            "current_product_code": "CURRENT_PRODUCT_CODE",
            "effective_date": "tomorrow",
            "fiber_linked": "",
            "subscription_email": "fakeemail@email.coop",
            "language": "es_ES",
        }

        ChangeTariffTicket(
            username, customer_code, fields_dict, override_ticket_ids=[1, 2]
        ).create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        calls = [
            mocker.call(
                "ProcessManagementProcessID", ChangeTariffTicketConfiguration.process_id
            ),
            mocker.call(
                "ProcessManagementActivityID",
                ChangeTariffTicketConfiguration.activity_id,
            ),
            mocker.call("renovaCanviTarifa", "1"),
            mocker.call("liniaMobil", "666666666"),
            mocker.call("productMobil", "NEW_PRODUCT_CODE"),
            mocker.call("tarifaAntiga", "CURRENT_PRODUCT_CODE"),
            mocker.call("dataExecucioCanviTarifa", "tomorrow"),
            mocker.call("correuElectronic", "fakeemail@email.coop"),
            mocker.call("idioma", "es_ES"),
            mocker.call("enviarNotificacio", "1"),
        ]
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.create_otrs_process_ticket.assert_called_once_with(  # noqa
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls],
        )

    def test_get_search_args(self):
        username = "7456787G"
        customer_code = "1234"

        search_args = ChangeTariffTicket(
            username, customer_code, fields_dict={}
        ).get_search_args()
        assert (
            search_args["dynamic_fields"][0].value
            == ChangeTariffTicketConfiguration.process_id
        )
        assert (
            search_args["dynamic_fields"][1].value
            == ChangeTariffTicketConfiguration.activity_id
        )
        assert search_args["Queues"][0] == ChangeTariffTicketConfiguration.queue
        assert search_args["States"][0] == ChangeTariffTicketConfiguration.state


class TestCaseChangeTariffExceptionalTicket:
    def test_create(self, mocker):
        username = "7456787G"
        customer_code = "1234"

        OTRSClientMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient",
            return_value=mocker.Mock(),
        )
        TicketMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket",
            return_value=mocker.Mock(),
        )
        ArticleMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article",
            return_value=mocker.Mock(),
        )
        DynamicFieldMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField",
            return_value=mocker.Mock(),
        )

        expected_ticket_data = {
            "Title": "Sol·licitud Canvi de tarifa excepcional",
            "Queue": ChangeTariffExceptionalTicketConfiguration.queue,
            "State": ChangeTariffExceptionalTicketConfiguration.state,
            "Type": ChangeTariffExceptionalTicketConfiguration.type,
            "Priority": ChangeTariffExceptionalTicketConfiguration.priority,
            "CustomerUser": customer_code,
            "CustomerID": customer_code,
        }
        expected_article_data = {
            "Subject": "Sol·licitud Canvi de tarifa excepcional",
            "Body": "-",
        }

        fields_dict = {
            "phone_number": "666666666",
            "new_product_code": "NEW_PRODUCT_CODE",
            "current_product_code": "CURRENT_PRODUCT_CODE",
            "effective_date": "tomorrow",
            "fiber_linked": "28",
            "subscription_email": "fakeemail@email.coop",
            "language": "ca_ES",
            "send_notification": True,
        }

        ChangeTariffExceptionalTicket(username, customer_code, fields_dict).create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        calls = [
            mocker.call(
                "ProcessManagementProcessID",
                ChangeTariffExceptionalTicketConfiguration.process_id,
            ),
            mocker.call(
                "ProcessManagementActivityID",
                ChangeTariffExceptionalTicketConfiguration.activity_id,
            ),
            mocker.call("renovaCanviTarifa", "0"),
            mocker.call("liniaMobil", "666666666"),
            mocker.call("productMobil", "NEW_PRODUCT_CODE"),
            mocker.call("tarifaAntiga", "CURRENT_PRODUCT_CODE"),
            mocker.call("dataExecucioCanviTarifa", "tomorrow"),
            mocker.call("OdooContractRefRelacionat", "28"),
            mocker.call("correuElectronic", "fakeemail@email.coop"),
            mocker.call("idioma", "ca_ES"),
            mocker.call("enviarNotificacio", "1"),
        ]
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.create_otrs_process_ticket.assert_called_once_with(  # noqa
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls],
        )

    def test_create_with_shared_bond_id(self, mocker):
        username = "7456787G"
        customer_code = "1234"

        OTRSClientMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient",
            return_value=mocker.Mock(),
        )
        OTRSClientMock.return_value.create_otrs_process_ticket.return_value = (
            mocker.Mock(spec=["id"])
        )
        OTRSClientMock.return_value.create_otrs_process_ticket.return_value.id = "1"

        TicketMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket",
            return_value=mocker.Mock(),
        )
        ArticleMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article",
            return_value=mocker.Mock(),
        )
        DynamicFieldMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField",
            return_value=mocker.Mock(),
        )

        expected_ticket_data = {
            "Title": "Sol·licitud Canvi de tarifa oficina virtual",
            "Queue": ChangeTariffTicketConfiguration.queue,
            "State": ChangeTariffTicketConfiguration.state,
            "Type": ChangeTariffTicketConfiguration.type,
            "Priority": ChangeTariffTicketConfiguration.priority,
            "CustomerUser": customer_code,
            "CustomerID": customer_code,
        }
        expected_article_data = {
            "Subject": "Sol·licitud Canvi de tarifa oficina virtual",
            "Body": "-",
        }

        fields_dict = {
            "phone_number": "666666666",
            "new_product_code": "NEW_PRODUCT_CODE",
            "current_product_code": "CURRENT_PRODUCT_CODE",
            "effective_date": "tomorrow",
            "fiber_linked": "",
            "subscription_email": "fakeemail@email.coop",
            "language": "ca_ES",
            "send_notification": False,
            "shared_bond_id": "C03457456M",
        }

        ticket = ChangeTariffTicket(username, customer_code, fields_dict).create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        calls = [
            mocker.call(
                "ProcessManagementProcessID", ChangeTariffTicketConfiguration.process_id
            ),
            mocker.call(
                "ProcessManagementActivityID",
                ChangeTariffTicketConfiguration.activity_id,
            ),
            mocker.call("renovaCanviTarifa", "0"),
            mocker.call("liniaMobil", "666666666"),
            mocker.call("productMobil", "NEW_PRODUCT_CODE"),
            mocker.call("tarifaAntiga", "CURRENT_PRODUCT_CODE"),
            mocker.call("dataExecucioCanviTarifa", "tomorrow"),
            mocker.call("correuElectronic", "fakeemail@email.coop"),
            mocker.call("idioma", "ca_ES"),
            mocker.call("enviarNotificacio", "0"),
            mocker.call("IDAbonamentCompartit", "C03457456M"),
        ]
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.create_otrs_process_ticket.assert_called_once_with(  # noqa
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls],
        )
        assert ticket.id == "1"
