from django_silica.SilicaComponent import SilicaComponent


# noinspection PyMethodOverriding
class Redirect(SilicaComponent):
    def redirect_me(self, path):
        self.redirect(path)
        pass

    def inline_template(self):
        return """
            <div class="p-5 border m-5">
                <p>I will be redirected!</p>
            </div>
        """
