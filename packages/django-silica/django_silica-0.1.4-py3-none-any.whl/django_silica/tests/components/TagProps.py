from django_silica.SilicaComponent import SilicaComponent


class TagProps(SilicaComponent):
    bool_val: bool = False
    no_value = None
    # int_val: int = 0
    # float_val: float = 0.0
    # str_val: str = ""
    # list_val: list = []
    # dict_val: dict = {}
    # none_val: None = None

    def inline_template(self):
        return """
            <div>   
                bool_val: {{ bool_val }}<br>
                no_value: {{ no_value }}<br>
            </div>
        """