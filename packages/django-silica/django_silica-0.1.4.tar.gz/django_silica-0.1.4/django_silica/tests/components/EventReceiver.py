from django_silica.SilicaComponent import SilicaComponent


class EventReceiver(SilicaComponent):
    payload = None

    def on_event_name(self, payload):
        self.payload = payload
        self.js_call("alert", "event_name called!")

    def inline_template(self):
        return """<div>Received payload! {{ payload }}</div>"""
