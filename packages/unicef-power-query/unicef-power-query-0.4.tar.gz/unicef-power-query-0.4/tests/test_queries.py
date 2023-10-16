from io import BytesIO

from django.test import override_settings, TestCase

from PyPDF2 import PdfReader

from power_query.defaults import create_defaults
from power_query.fixtures import (
    FormatterFactory,
    QueryFactory,
    ReportFactory,
    UserFactory,
)
from power_query.models import Formatter, Query, Report


@override_settings(POWER_QUERY_DB_ALIAS="default")
class TestPowerQuery(TestCase):
    databases = {"default"}

    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = UserFactory(is_superuser=True, is_staff=True, is_active=True)
        cls.user1 = UserFactory(is_superuser=False, is_staff=False, is_active=True)
        cls.user2 = UserFactory(is_superuser=False, is_staff=False, is_active=True)
        create_defaults()
        cls.query1: Query = QueryFactory(
            name="Query1",
            code="result=conn.all()",
        )
        cls.query2: Query = QueryFactory(
            name="Query2", code=f"result=invoke({cls.query1.pk}, arguments)"
        )
        cls.formatter: Formatter = FormatterFactory(name="Queryset To HTML")
        cls.report: Report = ReportFactory(formatter=cls.formatter, query=cls.query1)
        cls.pdf_formatter: Formatter = FormatterFactory(
            name="Queryset To PDF",
            content_type="pdf",
            code="""
                <h1>{{ dataset.query.name }}1</h1>
                <table>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                {% if dataset.data %}
                        <tr>
                        <th>Number</th>

                        {% for key, value in dataset.data.0.items %}
                        {% endfor %}
                        </tr>
                    {% endif %}

                    {% for row in dataset.data %}
                    <tr>
                        <td>{{ forloop.counter }}</td>
                        {% for key, value in row.items %}
                            <td>
                                {% if value|date:"Y-m-d" %}
                                    {{ value|date:"Y-m-d" }}
                                {% else %}
                                    {{ value }}
                                {% endif %}
                            </td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
            """,
        )

        cls.pdf_report: Report = ReportFactory(
            formatter=cls.pdf_formatter, query=cls.query1
        )

    def test_query_execution(self) -> None:
        result = self.query1.execute_matrix()
        self.assertTrue(self.query1.datasets.exists())
        self.assertEqual(result["{}"], self.query1.datasets.first().pk)

    def test_query_lazy_execution(self) -> None:
        self.query1.execute_matrix()
        ds1 = self.query1.datasets.first()
        ds2, __ = self.query1.run(use_existing=True)
        self.assertEqual(ds1.pk, ds2.pk)

    def test_report_execution(self) -> None:
        self.query1.execute_matrix()
        dataset = self.query1.datasets.first()
        self.report.execute()
        self.assertTrue(self.report.documents.filter(dataset=dataset).exists())

    def test_nested_query(self) -> None:
        result = self.query2.execute_matrix()
        self.assertTrue(self.query2.datasets.exists())
        self.assertEqual(result["{}"], self.query2.datasets.first().pk)

    def test_pdf_report_execution(self) -> None:
        self.query1.execute_matrix()
        dataset = self.query1.datasets.first()
        self.pdf_report.execute()

        self.assertTrue(self.pdf_report.documents.filter(dataset=dataset).exists())

        document = self.pdf_report.documents.filter(dataset=dataset).first()

        self.assertEqual(document.content_type, "pdf")

        pdf_content = BytesIO(document.data)

        pdf_content = BytesIO(document.data)
        pdf_reader = PdfReader(pdf_content)

        self.assertTrue(len(pdf_reader.pages) > 0)

        page = pdf_reader.pages[0]
        page_text = page.extract_text()
        print(page_text)
        self.assertTrue("Query1" in page_text)
