import json
import random
from typing import List

from django_silica.EventManager import test_event
from django_silica.SilicaComponent import SilicaComponent


class CacheOps(SilicaComponent):
    first_name: str = "Simon"

    def inline_template(self):
        return """
            <div>
                {{ first_name }}
            </div>            
            """