from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.SilicaComponent import SilicaComponent


class QueryParams(SilicaComponent):
    property_1 = "foo"

    query_params = ["property_1"]

    def inline_template(self):
        return """
            <div>{{ property_1 }}</div>
        """



class QueryParamTests(SilicaTestCase):
    def test_query_params_can_be_set(self):
        (
            SilicaTest(component=QueryParams)
            .assertSet("property_1", "foo")
            .assertSee("foo")
        )

        request = RequestFactory().get("/?property_1=bar")
        request.user = AnonymousUser()

        (
            SilicaTest(component=QueryParams, request=request)
            .assertSet("property_1", "bar")
            .assertSee("bar")
        )
