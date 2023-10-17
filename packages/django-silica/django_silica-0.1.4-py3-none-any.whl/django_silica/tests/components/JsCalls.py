from django_silica.SilicaComponent import SilicaComponent


class JsCalls(SilicaComponent):
    def set_js_call(self):
        self.js_call("alert", "hi")

    def inline_template(self):
        return "<div>testing</div>"
