from django.urls import path

from django_silica.tests.components.Lifecycle import Lifecycle

urlpatterns = [
    path("lifecycle", Lifecycle.as_view(), name="lifecycle"),
    # ... add more testing URLs as needed
]
