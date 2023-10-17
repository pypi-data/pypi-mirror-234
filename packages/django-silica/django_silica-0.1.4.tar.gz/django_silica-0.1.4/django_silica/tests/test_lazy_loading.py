from django.test import TestCase, RequestFactory, Client, override_settings

from django_silica.SilicaComponent import SilicaComponent
from django_silica.tests.SilicaTestCase import SilicaTest


class LazyLoading(SilicaComponent):

    is_mounted: bool = False

    def mount(self):
        self.is_mounted = True

    def inline_template(self):
        # language=html
        return """
            <div>   
                <h1>I will be lazy loaded!</h1>requi
            </div>
        """

    def inline_placeholder(self):
        # language=html
        return """
            <div>
                <h1>Loading...</h1>
            </div>
        """

class TestLazyLoading(TestCase):
    def test_mount_is_not_called(self):
        (
            SilicaTest(component=LazyLoading, lazy=True)
            .assertSet("is_mounted", False)
        )

    def test_mount_is_called_on_non_lazy(self):
        (
            SilicaTest(component=LazyLoading, lazy=False)
            .assertSet("is_mounted", True)
        )

    def test_placeholder_is_seen(self):
        (
            SilicaTest(component=LazyLoading, lazy=True)
            .assertSee("Loading...")
        )

    def test_placeholder_is_not_seen_on_non_lazy(self):
        (
            SilicaTest(component=LazyLoading, lazy=False)
            .assertDontSee("Loading...")
        )

    def test_silica_lazy_attribute_is_present_on_initial_render(self):
        (
            SilicaTest(component=LazyLoading, lazy=True)
            .assertSee("silica:lazy")
        )

    def test_silica_lazy_attribute_is_not_present_on_initial_render_on_non_lazy(self):
        (
            SilicaTest(component=LazyLoading, lazy=False)
            .assertDontSee("silica:lazy")
        )
