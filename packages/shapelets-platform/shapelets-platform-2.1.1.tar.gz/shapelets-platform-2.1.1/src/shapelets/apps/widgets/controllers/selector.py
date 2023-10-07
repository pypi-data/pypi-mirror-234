from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget


@dataclass
class Selector(StateControl):
    """
    Creates a dropdown menu for displaying multiple choices.

    Parameters
    ----------
    options : int, float, str or any, optional
        A list of items to be chosen.

    title : str,  optional
        String with the Selector title. It will be placed on top of the Selector.

    placeholder : str,  optional
        Text showed inside the Selector by default.

    label_by : str,  optional
        Selects key to use as label.

    value_by : str,  optional
        Selects key to use as value.

    default : str, int, float or list,  optional
        Default value.

    allow_multi_selection : bool, optional
        Allows selecting multiple values.

    Returns
    -------
    Selector

    Examples
    --------
    >>> selector = app.selector(title="My Selector", options=['a','b','c']) 


    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * str
        * int
        * float
        * list
        * :func:`~shapelets.apps.DataApp.selector`

    .. rubric:: Bindable as 

    You can bind this widget as: 

    .. hlist::
        :columns: 1

        * tuple
    """

    options: Optional[List[Union[int, float, str]]] = None
    title: Optional[str] = None
    placeholder: Optional[str] = None
    default: Optional[Union[str, int, float]] = None
    allow_multi_selection: Optional[bool] = None
    width: Optional[Union[int, float]] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())
        # Check value is inside options
        self._check_value()
        if self.options is not None:
            self._add_index()

    def _add_index(self):
        """
        Add internal index to the data provided by the user.
        For example:
            user_input: ["A", "B", "C"]
            shapelets_transformation = {0: "A", 1: "B", 2: "C"}
        """
        adjust_default = []
        adjust_options = {}
        for index, item in enumerate(self.options):
            adjust_options[index] = item
            if self.default is not None:
                if isinstance(self.default, list) and item in self.default:
                    adjust_default.append([index, item])
                elif self.default == item:
                    adjust_default.extend([index, item])
        self.options = adjust_options
        if adjust_default:
            self.default = adjust_default
        elif not adjust_default and self.placeholder is None:
            # if there is no default and no placeholder, set default to the first option, but check first for multi selection
            if self.allow_multi_selection:
                # Send as list of list
                self.default = [[0, adjust_options[0]]]
            else:
                self.default = [0, adjust_options[0]]

    def replace_widget(self, new_widget: Selector):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.options = new_widget.options
        self.title = new_widget.title
        self.placeholder = new_widget.placeholder
        self.default = new_widget.default
        self.allow_multi_selection = new_widget.allow_multi_selection
        self.width = new_widget.width

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.default is not None:
            return self.default
        return None

    def from_string(self, string: str) -> Selector:
        self.default = string
        return self

    def to_string(self) -> str:
        return str(self.default)

    def from_int(self, number: int) -> Selector:
        self.default = [number, self.options[number]]
        return self

    def to_int(self) -> int:
        return int(self.default[1])

    def from_float(self, number: float) -> Selector:
        self.default = number
        self._check_value()
        return self

    def to_float(self) -> float:
        return float(self.default)

    def from_list(self, input_list: List) -> Selector:
        new_values = []
        for index in input_list:
            new_values.append([index, self.options[index]])
        self.default = new_values
        self.allow_multi_selection = True
        return self

    def to_list(self) -> List:
        return list(self.default)

    def _check_value(self):
        if self.default is not None and self.options is not None:
            if isinstance(self.default, list):
                for item in self.default:
                    if item not in self.options:
                        raise Exception(f"Value {self.default} must be in Options: {self.options}.")
            else:
                # Check when value is not a list.
                if self.default not in self.options:
                    raise Exception(f"Value {self.default} must be in Options: {self.options}.")

    def to_dict_widget(self, selector_dict: dict = None):
        if selector_dict is None:
            selector_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Selector.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.options is not None:
            if isinstance(self.options, Widget):
                target = {"id": self.options.widget_id, "target": AttributeNames.OPTIONS.value}
                _widget_providers.append(target)
            else:
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.OPTIONS.value: self.options,
                })

        if self.title is not None:
            if isinstance(self.title, str):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title,
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.placeholder is not None:
            if isinstance(self.placeholder, str):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.PLACEHOLDER.value: self.placeholder,
                })
            elif isinstance(self.placeholder, Widget):
                target = {"id": self.placeholder.widget_id, "target": AttributeNames.PLACEHOLDER.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Placeholder value should be a string or another widget")

        if self.default is not None and self.default:
            if isinstance(self.default, Widget):
                target = {"id": self.default.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.default,
                })

        if self.allow_multi_selection is not None:
            if isinstance(self.allow_multi_selection, bool):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.ALLOW_MULTI_SELECTION.value: self.allow_multi_selection,
                })
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: allow_multi_selection value should be a string or another widget")

        if self.width is not None:
            if self.width > 100 or self.width < 0:
                raise ValueError("Width percentage cannot be higher than 100 or smaller than 0.")

            if isinstance(self.width, (int, float)):
                selector_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.WIDTH.value: self.width
                })
            elif isinstance(self.width, Widget):
                target = {"id": self.width.widget_id, "target": AttributeNames.WIDTH.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Width value should be a int or float or another widget")

        if _widget_providers:
            self.add_widget_providers(selector_dict, _widget_providers)

        return selector_dict


class SelectorWidget(Widget, Selector):

    def __init__(self,
                 options: Optional[List[Union[int, float, str]]] = None,
                 title: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 default: Optional[Union[str, int, float]] = None,
                 allow_multi_selection: Optional[bool] = None,
                 width: Optional[Union[int, float]] = None,
                 **additional):
        if placeholder is not None and default is not None:
            raise ValueError("Placeholder and default value cannot be assigned at the same time. Please, pick one.")

        Widget.__init__(self, Selector.__name__,
                        compatibility=tuple([str.__name__, int.__name__, float.__name__, list.__name__,
                                             List._name, Selector.__name__]),
                        **additional)
        Selector.__init__(self, options=options, title=title, placeholder=placeholder, default=default,
                          allow_multi_selection=allow_multi_selection, width=width)
        self._parent_class = Selector.__name__

    def to_dict_widget(self):
        selector_dict = Widget.to_dict_widget(self)
        selector_dict = Selector.to_dict_widget(self, selector_dict)
        return selector_dict
