import json
import re
from typing import Dict, Any

import shortuuid
from django.core.cache import cache
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.decorators import classonlymethod
from django.utils.module_loading import import_string
from django.views.generic import TemplateView

from django_silica.SilicaTemplateResponse import SilicaTemplateResponse
from django_silica.mixins.ValidatesProperties import ValidatesProperties
from django_silica.utils import pascal_to_snake
from django_silica.EventManager import EventManager


class SilicaComponent(TemplateView, ValidatesProperties):
    component_id: str = ""
    component_name: str = ""
    query_params: dict = {}
    has_rendered: bool = False
    js_calls: list = []
    event_calls: list = []
    lazy: bool = False

    def __init__(self, **kwargs):
        self.response_class = SilicaTemplateResponse

        self.component_id = ""
        self.component_key = ""
        self.component_name = ""
        self.lazy = False

        self.request: HttpRequest = None

        super().__init__(**kwargs)

        if "id" in kwargs:
            self.component_id = kwargs["id"]

        if "component_name" in kwargs:
            self.component_name = kwargs["component_name"]

        if "request" in kwargs:
            self.request = kwargs["request"]

        if "lazy" in kwargs:
            self.lazy = kwargs["lazy"]

        assert self.component_id != "", "Component id must be set"
        assert self.component_name != "", "Component name must be set"

        self._set_template()

    def _set_template(self):
        """Either template_name was provided, or inline_template was provided, or we'll set the template_name based on the component name."""
        # check if lazy loading, if so, set template_name to placeholder
        if self.lazy:
            #todo, inline place holder -> user placeholder -> framework placeholder
            if inline_placeholder := self.inline_placeholder():
                self.template_name = f"::infabrica-inline::{inline_placeholder}"
                return
            # else:
            #     self.template_name = "silica/placeholder.html"
            # return

        if self.template_name:
            return

        if inline_template := self.inline_template():
            self.template_name = f"::infabrica-inline::{inline_template}"
            return

        self.template_name = f"silica/{self.get_template_name()}"

    def inline_template(self):
        pass

    def inline_placeholder(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["component_id"] = self.component_id

        # Load local attributes into context
        local_state = self._local_state()

        # Loading state from cache into context
        cached_state = self.get_state()

        state = {**local_state, **cached_state}

        for key, value in state.items():
            context[key] = value

        # Set authenticated user
        if self.request and self.request.user.is_authenticated:
            context["user"] = self.request.user

        return context

    def _local_state(self):
        state = {}
        for attr in dir(self):
            if not self._is_public(attr):
                continue
            try:
                value = getattr(self, attr)
                if (
                    not attr.startswith("_")
                    and not callable(value)
                    and not isinstance(
                        getattr(SilicaComponent, attr, None), classonlymethod
                    )
                ):
                    state[attr] = value
            except AttributeError as e:
                print(f"Issue with attribute: {attr} - Error: {e}")

        return state

    def store_state(self):
        # Extracting non-private and non-callable attributes for state
        state = self._local_state()

        cache.set(f"silica:component:{self.component_id}", state)

    def get_state(self):
        return cache.get(f"silica:component:{self.component_id}", {})

    def get_template_name(self):
        return pascal_to_snake(self.__class__.__name__) + ".html"

    def render(self, init_js=False, extra_context=None, request=None, lazy=False) -> str:
        """prepare context and render component in a response"""

        if extra_context is not None:
            self.extra_context = extra_context

        if request:
            self.request = request

        context = self.get_context_data()
        context.update(
            {
                "js_calls": self.js_calls,
                "event_calls": self.event_calls,
            }
        )

        response = self.render_to_response(
            context=context,
            component=self,
            init_js=init_js,
            lazy=lazy,
        )

        if hasattr(response, "render"):
            response.render()

        rendered_component = response.content.decode("utf-8")

        return rendered_component

    @classonlymethod
    def as_view(cls, **initkwargs):
        """This is the first point into a Django view, ensure name is provided from url and initiate ID is set before the view is called."""
        if "component_id" not in initkwargs:
            initkwargs["component_id"] = str(shortuuid.uuid())

        if "component_name" not in initkwargs:
            # Convert the class name from CamelCase to snake_case
            initkwargs["component_name"] = re.sub(
                r"(?<!^)(?=[A-Z])", "-", cls.__name__
            ).lower()

        return super().as_view(**initkwargs)

    @staticmethod
    def create(
        component_id: str,
        component_name: str,
        component_key: str = "",  # will be needed sooner or later
        request: HttpRequest = None,  # possibly need this for processing requests sent to the component
        kwargs: Dict[str, Any] = {},
    ) -> "SilicaComponent":

        if "lazy" in kwargs:
            lazy = kwargs["lazy"]
        else:
            lazy = False

        ComponentClass = import_string(component_name)
        component_instance = ComponentClass(
            component_id=component_id,
            component_name=component_name,
            lazy=lazy,
        )
        component_instance._set_state_from_cache()
        component_instance.js_calls = []
        component_instance.event_calls = []

        # Set attributes from {% infabrica .. %} tag
        for key, value in kwargs.items():
            if component_instance._is_public(key):
                setattr(component_instance, key, value)

        return component_instance

    def _set_state_from_cache(self):
        """
        Load state from cache into component instance.
        """
        state = self.get_state()
        for key, value in state.items():
            setattr(self, key, value)

    def render_to_string(self):
        template_name = f"silica/{self.get_template_name()}"
        return render_to_string(template_name, self.get_context_data())

    def reset_js_calls(self):
        self.js_calls = []

    # def get_template_names(self):
    #     # Return the inline template as if it was a template name
    #     # Our custom loader will handle it properly
    #     return ["Hello, {{ name }}!"]

    def dispatch(self, request, *args, **kwargs):
        """
        Called by the `as_view` class method when utilizing a component directly as a view.
        """

        # how to provide request in kwargs to mount()?
        self.request = request

        if not self.lazy:
            self.mount()

        # if any get variables match public, and exist on the instance, then set them
        for key, value in request.GET.items():
            if self._is_public(key) and hasattr(self, key):
                setattr(self, key, value)

        # We'll call some lifecycle hooks here

        # self.hydrating()
        context = self.get_context_data()
        context.update({"js_calls": self.js_calls})
        context.update({"event_calls": self.event_calls})

        self.store_state()

        rendered_response = self.render_to_response(
            context=context,
            component=self,
            init_js=True,
        )

        return rendered_response


    # def render_to_response(self, context, **response_kwargs):
    #     """
    #     Override the default render_to_response method to control the initial rendered content of the component.
    #     """
    #     response_kwargs.setdefault("content_type", self.content_type)
    #     return self.response_class(
    #         request=self.request,
    #         template=self.get_template_names(),
    #         context=context,
    #         using=self.template_engine,
    #         **response_kwargs,
    #     )

    def _is_public(self, name: str) -> bool:
        """
        Determines if the name should be sent in the context.
        """

        # Ignore some standard attributes from TemplateView

        protected_names = (
            "render",
            "request",
            "as_view",
            "view",
            "args",
            "kwargs",
            "content_type",
            "extra_context",
            "http_method_names",
            "template_engine",
            "template_name",
            "dispatch",
            "id",
            "get",
            "get_context_data",
            "get_template_names",
            "render_to_response",
            "http_method_not_allowed",
            "options",
            "setup",
            "fill",
            "view_is_async",
            # Component methods
            "component_id",
            "component_name",
            "component_key",
            "reset",
            "mount",
            "hydrate",
            "updating",
            "update",
            "calling",
            "called",
            "complete",
            "rendered",
            "parent_rendered",
            "validate",
            "is_valid",
            "get_frontend_context_variables",
            "errors",
            "updated",
            "parent",
            "children",
            "call",
            "js_calls",
            "event_calls",
            "component_cache_key",
            "inline_template",
            "placeholder"
        )
        # We'll need a way to exclude certain props from being sent to the front
        # excludes = []

        # When we create hook methods, we'll also need to exclude them
        # hooks = []

        return not (
            name.startswith("_")
            or name in protected_names
            # or name in excludes
        )

    def js_call(self, method, *args, **kwargs):
        self.js_calls.append(
            {
                "fn": method,
                "args": args,
                "kwargs": kwargs,
            }
        )

    # Events
    def emit(self, event_name, payload: Dict = None):
        """Emit to all component present in the DOM"""
        self.event_calls.append(
            {
                "type": "emit",
                "name": event_name,
                "payload": payload,
            }
        )

    def emit_to(self, component_name, event_name, payload: Dict = None):
        """Emit to a specific component in the dom"""
        self.event_calls.append(
            {
                "type": "emit_to",
                "component_name": component_name,
                "name": event_name,
                "payload": payload
            }
        )

    def receive_event(self, event_name, payload):
        # if we have a listener for this event, call it
        if hasattr(self, event_name) and callable(getattr(self, event_name)):
            getattr(self, event_name)(payload)

    def get_absolute_path(self):
        module_name = (
            self.__module__
        )  # gives the module name in which the class is defined
        class_name = self.__class__.__name__  # gives the name of the class
        return f"{module_name}.{class_name}"

    # Hooks
    def mount(self):
        pass

    def rendered(self, html):
        """
        Hook that gets called after the component has been rendered.
        """
        pass

    def redirect(self, url):
        self.js_call("_silicaRedirect", url)

    def jsonable_state(self):
        state = self.get_context_data()

        for key, value in state.copy().items():
            if not self._is_jsonable(value):
                del state[key]

        return state

    def _is_jsonable(self, x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False

    def __repr__(self):
        return f"ComponentRequest(name='{self.component_name}' id='{self.component_id}'"