# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class History(Component):
    """A History component.
Component to serve as a history explorer

Keyword arguments:

- id (string; required):
    Unique ID to identify this component in Dash callbacks.

- dashpoolEvent (dict; optional):
    latest Dashpool Event.

    `dashpoolEvent` is a dict with keys:

    - data (boolean | number | string | dict | list; optional)

    - timestamp (dict; required)

        `timestamp` is a dict with keys:

        - toExponential (required):
            Returns a string containing a number represented in
            exponential notation. @,param,fractionDigits, ,Number of
            digits after the decimal point. Must be in the range 0 -
            20, inclusive.

        - toFixed (required):
            Returns a string representing a number in fixed-point
            notation. @,param,fractionDigits, ,Number of digits after
            the decimal point. Must be in the range 0 - 20, inclusive.

        - toLocaleString (dict; optional):
            Converts a number to a string by using the current or
            specified locale. @,param,locales, ,A locale string or
            array of locale strings that contain one or more language
            or locale tags. If you include more than one locale
            string, list them in descending order of priority so that
            the first entry is the preferred locale. If you omit this
            parameter, the default locale of the JavaScript runtime is
            used. @,param,options, ,An object that contains one or
            more properties that specify comparison options.
            @,param,locales, ,A locale string, array of locale
            strings, Intl.Locale object, or array of Intl.Locale
            objects that contain one or more language or locale tags.
            If you include more than one locale string, list them in
            descending order of priority so that the first entry is
            the preferred locale. If you omit this parameter, the
            default locale of the JavaScript runtime is used.
            @,param,options, ,An object that contains one or more
            properties that specify comparison options.

            `toLocaleString` is a dict with keys:


        - toPrecision (required):
            Returns a string containing a number represented either in
            exponential or fixed-point notation with a specified
            number of digits. @,param,precision, ,Number of
            significant digits. Must be in the range 1 - 21,
            inclusive.

        - toString (optional):
            Returns a string representation of an object.
            @,param,radix, ,Specifies a radix for converting numeric
            values to strings. This value is only used for numbers.

        - valueOf (optional):
            Returns the primitive value of the specified object.

    - type (string; required)

- n_refreshed (number; optional):
    : An integer that represents the number of times that this element
    has been refreshed.

- nodes (list of dicts; optional):
    Array of nodes shown in the Tree View.

    `nodes` is a list of dicts with keys:

    - app (string; optional)

    - data (boolean | number | string | dict | list; optional)

    - frame (string; optional)

    - icon (string; optional)

    - id (string; required)

    - label (string; required)

    - layout (string; optional)

    - parent (string; optional)

    - shared (list of strings; optional)

    - type (string; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'History'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, nodes=Component.UNDEFINED, n_refreshed=Component.UNDEFINED, dashpoolEvent=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'dashpoolEvent', 'n_refreshed', 'nodes']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'dashpoolEvent', 'n_refreshed', 'nodes']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(History, self).__init__(**args)
