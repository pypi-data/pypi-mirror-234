from django_silica.SilicaComponent import SilicaComponent


class EventSender(SilicaComponent):
    payload = None

    def send_event(self):
        self.emit("on_event_name", {'msg': "Hello World!"})

    def inline_template(self):
        return """<div><a href="#" silica:click.prevent="send_event">Send event</a></div>"""
