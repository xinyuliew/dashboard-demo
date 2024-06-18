# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ReactTable(Component):
    """A ReactTable component.


Keyword arguments:

- id (string; required)

- rows (list of dicts; required)

    `rows` is a list of dicts with keys:

    - date (string; required)

    - id (string; required)

    - num_replies (number; required)

    - replies (list of dicts; optional)

        `replies` is a list of dicts with keys:

        - date (string; required)

        - id (string; required)

        - num_replies (number; required)

        - replies (list; optional)

        - sentiment (string; required)

        - stance (string; required)

        - text (string; required)

    - sentiment (string; required)

    - stance (string; required)

    - text (string; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'collapsible_table'
    _type = 'ReactTable'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, rows=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'rows']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'rows']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'rows']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ReactTable, self).__init__(**args)
