from __future__ import annotations

import json

import urllib.parse
from typing import Type

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from django.template.response import TemplateResponse


class SilicaTemplateResponse(TemplateResponse):
    def __init__(
        self,
        request,
        template,
        context=None,
        content_type=None,
        status=None,
        charset=None,
        using=None,
        headers=None,
        component: "SilicaComponent" = None,
        init_js=False,
        lazy=False,
    ):
        super().__init__(
            template=template,
            request=request,
            context=context,
            content_type=content_type,
            status=status,
            charset=charset,
            using=using,
        )
        self.component = component
        self.init_js = init_js
        self.lazy = lazy

    def render(self):
        response = super().render()

        if not self.component or not self.component.component_id:
            return response

        template_string = response.content.decode("utf-8").strip()

        # Assuming there's only one root element in the template
        soup = BeautifulSoup(template_string, "html.parser")

        # todo: check and raise error for no root nodes found
        root_node = soup.contents[0]

        assert root_node, "Silica component must include a single root element"

        root_node.attrs["silica:id"] = self.component.component_id
        root_node.attrs["silica:name"] = self.component.component_name

        if self.init_js and not self.component.lazy:
            jsonable_state = self.component.jsonable_state()
            jsonable_state["js_calls"] = self.component.js_calls
            jsonable_state["event_calls"] = self.component.event_calls
            json_state = json.dumps(jsonable_state)
            encoded_state = urllib.parse.quote(json_state)
            root_node.attrs["silica:initial-data"] = encoded_state

        if self.component.lazy:
            root_node.attrs["silica:lazy"] = "true"
            # root_node.attrs["silica:initial-data"] = "{}"

        self.component.has_rendered = True

        soup.smooth()
        rendered_template = soup.encode(formatter=UnsortedAttributes()).decode("utf-8")

        self.component.rendered(rendered_template)
        self.component.store_state()

        response.content = rendered_template

        return response


class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == "m":
                continue
            yield k, v
