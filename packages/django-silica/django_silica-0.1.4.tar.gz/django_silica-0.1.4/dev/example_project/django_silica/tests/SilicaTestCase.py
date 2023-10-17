import json
from urllib.parse import unquote
from typing import Type, List, Dict

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import AnonymousUser

# from infabrica import settings
# todo, move to from django.conf import settings

from django_silica.SilicaComponent import SilicaComponent
from django_silica.views import message

from bs4 import BeautifulSoup

# current_templates = settings.TEMPLATES[0].copy()
# current_templates["DIRS"].append(
#     os.path.join(settings.BASE_DIR, "silica/tests/templates")
# )


# @override_settings(TEMPLATES=[current_templates])
class SilicaTestCase(TestCase):
    pass


# @override_settings(TEMPLATES=[current_templates])
class SilicaTest(TestCase):
    received_html = ""
    received_data = {}
    received_js_calls = []
    received_event_calls = []

    def __init__(
        self,
        component: Type[SilicaComponent],
        request: Type[WSGIRequest] = None,
        **kwargs
    ):
        super().__init__()

        if request is None:
            request = RequestFactory().get("/", **kwargs)
            request.user = AnonymousUser()

        response = component.as_view(**kwargs)(request)

        self.component = response.component
        self.received_html = response.render().content.decode("utf-8")

        # use beautiful soup to parse the html
        soup = BeautifulSoup(self.received_html, "html.parser")

        # extract the attribute: silica:initial-data from the root node
        root_node = soup.contents[0]
        initial_data = root_node.attrs.get("silica:initial-data", None)

        # uri decode the initial data
        if initial_data:
            initial_data_raw = unquote(initial_data)
            initial_data_parsed = json.loads(initial_data_raw)

            self.received_event_calls = initial_data_parsed.pop('event_calls')
            self.received_js_calls = initial_data_parsed.pop('js_calls')
            self.received_data = initial_data_parsed


    def call(self, method_name, *args, **kwargs):
        self._send_message(
            [{"type": "call_method", "method_name": method_name, "args": args}]
        )

        return self

    def set(self, prop, value):
        self._send_message([{"type": "set_property", "name": prop, "value": value}])

        return self

    def assertSet(self, prop, value):
        self.assertEqual(getattr(self.component, prop), value, msg=f'Property: {prop} is not set as "{value}"')
        return self

    def assertSee(self, text):
        assert text in self.received_html, f'"{text}" is not seen in the rendered html'
        return self

    def assertDontSee(self, text):
        assert text not in self.received_html, f'"{text}" is seen in the rendered html'
        return self

    def assertNone(self, prop):
        self.assertIsNone(getattr(self.component, prop, None))
        return self

    def assertJsCalled(self, fn_name, *args):
        self.assertTrue(
            type(self.received_js_calls) == list,
        )

        if args:
            condition = lambda call: call["fn"] == fn_name and call["args"] == list(
                args
            )
        else:
            condition = lambda call: call["fn"] == fn_name

        self.assertTrue(any(condition(call) for call in self.received_js_calls))

        return self

    def assertEventEmitted(self, event_name, event_payload = None):
        self.assertTrue(
            type(self.received_event_calls) == list,
            'event_calls not seen in the data'
        )

        # assert that a dict in list contains a key 'name' matching the event_name, optionally check if the event_payload matches too
        self.assertTrue(
            any(call['name'] == event_name and (event_payload is None or call['payload'] == event_payload) for call in self.received_event_calls),
            f'Event {event_name} not seen in the data'
        )

        return self

    def assertEventNotEmitted(self, event_name):
        self.assertTrue(
            type(self.received_event_calls) == list,
            'event_calls not seen in the data'
        )

        self.assertFalse(
            any(call['name'] == event_name for call in self.received_event_calls),
            f'Event {event_name} seen in the data'
        )

        return self

    def emit(self, event_name, payload):
        self._send_message([
            {
                "type": "event",
                "event_name": event_name,
                "payload": payload
            }
        ])

        return self

    def emit_to(self, event_name, payload):
        self._send_message([
            {
                "type": "event",
                "event_name": event_name,
                "payload": payload
            }
        ])

        return self

    def _send_message(self, actions: List):
        # prepare request
        data = json.dumps(
            {
                "id": self.component.component_id,
                "name": self.component.get_absolute_path(),
                "actions": actions,
            }
        )

        factory = RequestFactory()
        request = factory.post(
            "/silica/message", data, content_type="application/json"
        )
        request.user = AnonymousUser()

        json_response = message(request)
        data = json.loads(json_response.content.decode("utf-8"))

        self.received_html = data["html"]
        self.received_data = data["data"]
        self.received_js_calls = data["js_calls"]
        self.received_event_calls = data["event_calls"]

        # rehydrate the test component
        self.component._set_state_from_cache()
