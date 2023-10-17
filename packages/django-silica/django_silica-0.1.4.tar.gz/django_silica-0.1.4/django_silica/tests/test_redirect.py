from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.tests.components.Redirect import Redirect


class RedirectTest(SilicaTestCase):
    def test_redirect_from_method(self):
        (
            SilicaTest(component=Redirect)
            .call("redirect_me", "/redirected")
            .assertJsCalled("_silicaRedirect", "/redirected")
        )
