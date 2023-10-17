import random

from django_silica.SilicaComponent import SilicaComponent


class ChildComponent(SilicaComponent):
    child_prop = None
    rendered_count = 0

    def mount(self):
        self.child_prop = random.randint(0, 100)

    def rendered(self, html):
        self.rendered_count += 1

    def inline_template(self):
        return """
            <div class="p-5 my-3 border">
                <div class="text-sm text-gray-400">silica id: {{ component_id }}</div>
               I'm a child, i've been rendered {{ rendered_count }}!
               
               <p>my id: {{ child_prop }}</p>
               
               <input silica:model="child_prop" class="border border-gray-500 py-2 px-3 rounded" />
            </div>
        """
