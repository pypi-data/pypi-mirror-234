from django.test import override_settings, TestCase

from power_query.fixtures import ParametrizerFactory


@override_settings(POWER_QUERY_DB_ALIAS="default")
class TestPowerQuery(TestCase):
    databases = {"default"}

    def test_create_defaults(self) -> None:
        from power_query.defaults import create_defaults

        create_defaults()

    def test_parameter(self) -> None:
        p = ParametrizerFactory()
        p.refresh()
