from django_silica.SilicaComponent import SilicaComponent


class ParentComponent(SilicaComponent):
    def inline_template(self):
        return """
            <div class="p-5 border m-5">
                {% load silica %}
                
                <div class="text-sm text-gray-500">infabrica id: {{ component_id }}</div>
                
                <p>I'm a parent!</p>
                
                <div>{% silica "silica.tests.components.ChildComponent.ChildComponent" %}</div>
                <div>{% silica "silica.tests.components.ChildComponent.ChildComponent" %}</div>
            </div>
        """
