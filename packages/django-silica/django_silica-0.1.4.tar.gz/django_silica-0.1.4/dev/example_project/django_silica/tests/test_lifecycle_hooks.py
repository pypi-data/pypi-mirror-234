from django.test import RequestFactory, Client

from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.tests.components.Lifecycle import Lifecycle


class LifecycleTestCase(SilicaTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_mount_is_called_once(self):
        (
            # Initial request
            SilicaTest(component=Lifecycle)
            .assertSet("called_mount", 1)
            # Subsequent request to /message
            .set("test_property", "test")
            .assertSet("called_mount", 1)
        )

    def test_rendered(self):
        (SilicaTest(component=Lifecycle).assertSet("called_rendered", 1))

    def test_hooks_are_called_in_order(self):
        (
            SilicaTest(component=Lifecycle).assertSet("called_mount", 1)
            # .assertSet("called_rendering", 1)
            # .assertSet("called_rendered", 1)
            # .assertSet("called_hydrate", 1)
            # .assertSet("called_hydrate", 1)
            # .assertSet("called_updating_property", 0)
            # .assertSet("called_updated_property", 0)
            # .assertSet("called_updated", 0)
            # .assertSet("called_updated", 0)
        )
