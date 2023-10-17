from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.tests.components.InlineTemplate import InlineTemplate


class LifecycleTestCase(SilicaTestCase):
    def test_inline_template_is_rendered(self):
        SilicaTest(component=InlineTemplate).assertSee("Hello World!")

    def test_subsequent_requests_render_from_inline_template(self):
        (
            SilicaTest(component=InlineTemplate)
            .assertSee("Hello World!")
            .set("msg", "Goodbye World!")
            .assertSee("Goodbye World!")
        )
