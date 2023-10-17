from django.test import TestCase, RequestFactory, Client, override_settings

from django_silica.tests.SilicaTestCase import SilicaTest
from django_silica.tests.components.TagProps import TagProps


class TestTagProps(TestCase):
    def test_props_can_be_set_programmatically(self):
        (
            SilicaTest(component=TagProps, bool_val=None)
            .assertSet("bool_val", None)
        )

    def test_props_can_be_set_via_tag(self):
        client = Client()
        response = client.get("/silica/tests/tag-props")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bool_val: True")