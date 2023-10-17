from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.tests.components.Methods import Methods


class MethodsTestCase(SilicaTestCase):
    def test_method_calling_without_args(self):
        (
            SilicaTest(component=Methods)
            .assertSet("fruit", "banana")
            .assertSee("banana")
            .call("set_apple")
            .assertSet("fruit", "apple")
        )

    def test_method_calling_with_args(self):
        (
            SilicaTest(component=Methods)
            .call("set_fruit", "cherry")
            .assertSet("fruit", "cherry")
            .assertSee("cherry")
        )
