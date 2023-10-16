from django.http import HttpResponse
from django.test import override_settings, TestCase
from django.urls import reverse

from parameterized import parameterized

from power_query.defaults import create_defaults
from power_query.fixtures import (
    FormatterFactory,
    QueryFactory,
    ReportFactory,
    UserFactory,
)
from power_query.models import Report

CONTENT_TYPES = [
    ("application/json", "application/json"),
    ("text/html", "text/html; charset=utf-8"),
    ("text/plain", "text/plain"),
]


@override_settings(POWER_QUERY_DB_ALIAS="default")
class TestPowerQueryResponses(TestCase):
    databases = {"default"}

    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = UserFactory(is_superuser=True, is_staff=True, is_active=True)
        cls.user1 = UserFactory(
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        cls.user2 = UserFactory(is_superuser=False, is_staff=False, is_active=True)
        create_defaults()
        cls.formatter_json = FormatterFactory(
            name="Queryset To JSON", content_type="json", code=""
        )
        cls.query = QueryFactory()
        cls.report1: Report = ReportFactory(
            formatter=cls.formatter_json, query=cls.query, owner=cls.user1
        )
        cls.report2: Report = ReportFactory(
            formatter=cls.formatter_json, query=cls.query, owner=cls.user2
        )
        cls.report2.execute(run_query=True)

    @parameterized.expand(CONTENT_TYPES)
    def test_fetch_no_auth_content_types(self, accept: str, content_type: str) -> None:
        with self.settings(POWER_QUERY_DB_ALIAS="default"):
            url = reverse("power_query:data", args=[self.report2.pk])
            response = self.client.get(url, HTTP_ACCEPT=accept)
            self.assertEqual(response.status_code, 401)

    def test_report_view_superuser(self) -> None:
        with self.settings(POWER_QUERY_DB_ALIAS="default"):
            self.client.force_login(self.superuser)
            url = reverse("power_query:report", args=[self.report2.pk])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["report"], self.report2)
            self.assertTrue("documents" in response.context)

    def test_report_view_no_documents(self) -> None:
        with self.settings(POWER_QUERY_DB_ALIAS="default"):
            self.client.force_login(self.user1)
            url = reverse("power_query:report", args=[self.report1.pk])
            response: HttpResponse = self.client.get(url)
            self.assertEqual(response.status_code, 403, "User1 shouldn't access")
            url = reverse("power_query:report", args=[self.report2.pk])
            self.assertEqual(response.status_code, 403, "User1 should access")
