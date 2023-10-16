# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashpoolProvider(Component):
    """A DashpoolProvider component.
Context provider for easy interaction between Dashpool components

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers; required):
    Array of children.

- dragElement (boolean | number | string | dict | list; optional):
    The last drag element."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'DashpoolProvider'
    @_explicitize_args
    def __init__(self, children=None, dragElement=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'dragElement']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'dragElement']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(DashpoolProvider, self).__init__(children=children, **args)
