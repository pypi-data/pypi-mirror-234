from django_silica.SilicaComponent import SilicaComponent


class Properties(SilicaComponent):
    foo = "bar"

    def inline_template(self):
        return """
            <div>{{ foo }}</div>
        """
