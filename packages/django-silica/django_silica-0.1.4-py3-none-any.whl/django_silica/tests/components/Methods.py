from django_silica.SilicaComponent import SilicaComponent


class Methods(SilicaComponent):
    test_value = 1

    fruit = "banana"

    def set_apple(self):
        self.fruit = "apple"

    def set_fruit(self, fruit=""):
        self.fruit = fruit

    def inline_template(self):
        return """
            <div>
                {{ fruit }}
                <a silica:click="set_apple()">set apple</a>
            </div>        
        """

