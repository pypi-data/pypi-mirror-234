from django_silica.SilicaComponent import SilicaComponent


class Lifecycle(SilicaComponent):
    called_mount = 0
    called_hydrate = 0
    called_updating = 0
    called_updated = 0
    called_updating_property = 0
    called_updated_property = 0
    called_rendering = 0
    called_rendered = 0
    called_dehydrate = 0

    test_property = None

    def mount(self):
        self.called_mount += 1

    def hydrate(self):
        self.called_hydrate += 1

    def updating(self):
        self.called_updating += 1

    def updated(self):
        self.called_updated += 1

    def updating_property(self):
        self.called_updating_property += 1

    def updated_property(self):
        self.called_updated_property += 1

    def rendering(self):
        self.called_rendering += 1

    def rendered(self, html):
        self.called_rendered += 1

    def test_method(self):
        pass

    def inline_template(self):
        return """
            <div>
                hi!
            </div>        
        """