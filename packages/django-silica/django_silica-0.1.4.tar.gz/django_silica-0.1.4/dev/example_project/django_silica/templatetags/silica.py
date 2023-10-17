from typing import Dict

import shortuuid

from django_silica.call_method_parser import parse_kwarg, InvalidKwarg
from django_silica.errors import ComponentNotValid
from django_silica.SilicaComponent import SilicaComponent
from django import template

register = template.Library()


def silica(parser, token):

    parts = token.split_contents()

    if len(parts) < 2:
        raise template.TemplateSyntaxError(
            "%r tag requires at least a single argument" % token.contents.split()[0]
        )

    component_name = parser.compile_filter(parts[1])

    kwargs = {}

    # pass any other kwargs to component create
    for arg in parts[2:]:
        try:
            kwarg = parse_kwarg(arg)
            kwargs.update(kwarg)
        except InvalidKwarg:
            pass

    return SilicaNode(component_name=component_name, kwargs=kwargs)


register.tag("silica", silica)


class SilicaNode(template.Node):
    def __init__(self, component_name, kwargs: Dict = {}):
        self.component_name = component_name
        self.kwargs = kwargs
        self.component_key = ""
        self.parent = None

    def render(self, context, **kwargs):
        request = None

        if hasattr(context, "request"):
            request = context.request

        resolved_kwargs = {}
        for key, value in self.kwargs.items():
            try:
                resolved_value = template.Variable(value).resolve(context)

                if (
                    key == "parent"
                    and value == "view"
                    and not isinstance(resolved_value, SilicaComponent)
                ):
                    # Handle rendering a parent component from a template that is called from
                    # a `TemplateView`; for some reason `view` is clobbered in this instance, but
                    # the `silica` dictionary has enough data to instantiate a `Silica`
                    parent_component_data = template.Variable("silica").resolve(
                        context
                    )

                    resolved_value = SilicaComponent(
                        component_name=parent_component_data.get("component_name"),
                        component_id=parent_component_data.get("component_id"),
                        request=request,
                    )

                resolved_kwargs.update({key: resolved_value})
            except TypeError:
                resolved_kwargs.update({key: value})
            except template.VariableDoesNotExist:
                resolved_kwargs.update({key: value})

                if value.endswith(".id"):
                    pk_val = value.replace(".id", ".pk")

                    try:
                        resolved_kwargs.update(
                            {key: template.Variable(pk_val).resolve(context)}
                        )
                    except TypeError:
                        resolved_kwargs.update({key: value})
                    except template.VariableDoesNotExist:
                        resolved_kwargs.update({key: value})

        if "key" in resolved_kwargs:
            component_key = resolved_kwargs.pop("key")
        else:
            component_key = None

        if "lazy" in resolved_kwargs:
            lazy = resolved_kwargs.pop("lazy")
        else:
            lazy = False

        try:
            component_name = self.component_name.resolve(context)
        except AttributeError:
            raise ComponentNotValid(
                f"Component template is not valid: {self.component_name}."
            )

        resolved_kwargs.update({"lazy": lazy})

        component_id = shortuuid.uuid()

        self.view = SilicaComponent.create(
            component_id=component_id,
            component_name=component_name,
            component_key=component_key,
            kwargs=resolved_kwargs,
            request=request,
        )

        if request:
            for key, value in request.GET.items():
                if self.view._is_public(key) and hasattr(self.view, key):
                    setattr(self.view, key, value)

            self.request = request

        if not lazy:
            self.view.mount()

        rendered_component = self.view.render(init_js=True, request=request)

        return rendered_component
