import time

from django_silica.SilicaComponent import SilicaComponent


class Lazy(SilicaComponent):
    is_mounted: bool = False

    def mount(self):
        time.sleep(2)
        self.is_mounted = True

    def inline_template(self):
        return """
            <div>   
                <div silica:loading>Loading!</div>
                <h1>I will be lazy loaded! {{ is_mounted }}</h1>
            </div>
        """

    # def inline_placeholder(self):
    #     return """
    #         <div>
    #             <h1>Loading...</h1>
    #         </div>
    #     """
