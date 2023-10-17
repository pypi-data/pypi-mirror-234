from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.tests.components.Properties import Properties


class PropertiesTestCase(SilicaTestCase):
    def test_can_set_properties(self):
        (
            SilicaTest(component=Properties)
            .assertSet("foo", "bar")
            .assertSee("bar")
            .set("foo", "boo")
            .assertSet("foo", "boo")
            .assertSee("boo")
        )
