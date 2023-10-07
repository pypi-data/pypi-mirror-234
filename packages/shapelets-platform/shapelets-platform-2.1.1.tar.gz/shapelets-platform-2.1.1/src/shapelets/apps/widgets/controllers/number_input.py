from __future__ import annotations

import uuid

from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

from ...data_app_utils import TextStyle
from ..widget import AttributeNames, Widget, StateControl


@dataclass
class NumberInput(StateControl):
    """
    A basic widget for getting the user input as a number field.

    Parameters
    ----------
    title : str, optional
        String with the widget title. It will be placed on top of the widget box.

    value : int or float, optional
        Define number value.

    default_value : int or float, optional
        Default value for the widget.

    placeholder : str, optional
        Text showed inside the widget by default.

    min : int or float, optional
        Minimum value of the widget.

    max : int or float, optional
        Maximum value of the widget.

    step : int or float, optional
        The granularity the widget can step through values. Must greater than 0, and be divided by (max - min).

    text_style : dict, optional
        Dict to customize text: font size, font type y font style.

    units : str, optional
        Specifies the format of the value presented, for example %, KWh, Kmh, etc.


    Returns
    -------
    Number Input.

    Examples
    --------
    >>> number_input = app.number_input()

    >>> number_input = app.number_input(min=1,max=100,step=5,units='%')


    .. rubric:: Bind compatibility

    You can bind this widget with this:

    .. hlist::
        :columns: 1

        * int
        * float
        * :func:`~shapelets.apps.DataApp.number_input`

    .. rubric:: Bindable as

    You can bind this widget as:

    .. hlist::
        :columns: 1

        * int
        * float

    """
    title: Optional[str] = None
    value: Optional[Union[int, float]] = None
    default_value: Optional[Union[int, float]] = None
    placeholder: Optional[str] = None
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None
    text_style: Optional[TextStyle] = field(default_factory=lambda: TextStyle())
    units: Optional[str] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

        self.placeholder = "Place your number here" if self.placeholder is None else self.placeholder
        if self.value is not None:
            self._check_value()
            if self.max is not None and self.min is not None:
                if self.max < self.min:
                    raise ValueError("Max value cannot be lower than min")

                if self.value < self.min or self.value > self.max:
                    raise ValueError("Value must be between min and max")

                if self.default_value is not None:
                    if self.default_value < self.min or self.default_value > self.max:
                        raise ValueError("Default value must be between min and max")

    def replace_widget(self, new_widget: NumberInput):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.value = new_widget.value
        self.default_value = new_widget.default_value
        self.placeholder = new_widget.placeholder
        self.min = new_widget.min
        self.max = new_widget.max
        self.step = new_widget.step
        self.text_style = new_widget.text_style
        self.units = new_widget.units

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        elif self.default_value is not None:
            return self.default_value
        return None

    def from_int(self, number: int) -> NumberInput:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> NumberInput:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    def _check_value(self):

        if (self.value is not None and self.max is not None and self.min is not None):
            if isinstance(self.value, int) or isinstance(self.value, float):
                if (self.max < self.min):
                    raise ValueError("min property cannot be bigger than max")

                if (self.step is not None):
                    if (self.step != 0):
                        if (self.max - self.min) % self.step != 0:
                            raise ValueError("The (max-min) value should be divisible by the step value")
                    else:
                        raise ValueError("step property cannot be zero")

    def to_dict_widget(self, number_dict: dict = None):
        if number_dict is None:
            number_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: NumberInput.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []
        if self.value is not None:
            if isinstance(self.value, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.value.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.value}: value should be int, flot or another widget")

        if self.title is not None:
            if isinstance(self.title, str):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be string or another widget")

        if self.max is not None:
            if isinstance(self.max, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX.value: self.max
                })
            elif isinstance(self.max, Widget):
                target = {"id": self.max.widget_id, "target": AttributeNames.MAX.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Max value should be int, flot or another widget")

        if self.min is not None:
            if isinstance(self.min, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN.value: self.min
                })
            elif isinstance(self.min, Widget):
                target = {"id": self.min.widget_id, "target": AttributeNames.MIN.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Min value should be int, flot or another widget")

        if self.step is not None:
            if isinstance(self.step, (int, float)):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.STEP.value: self.step
                })
            elif isinstance(self.step, Widget):
                target = {"id": self.step.widget_id, "target": AttributeNames.STEP.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Step value should be int, flot or another widget")

        if self.placeholder is not None:
            if isinstance(self.placeholder, str):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.PLACEHOLDER.value: self.placeholder
                })
            elif isinstance(self.placeholder, Widget):
                target = {"id": self.placeholder.widget_id, "target": AttributeNames.PLACEHOLDER.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Placeholder should be string or another widget")

        if self.text_style is not None:
            if isinstance(self.text_style, dict):
                for key, value in self.text_style.items():
                    number_dict[AttributeNames.PROPERTIES.value].update({
                        key: value
                    })

        if self.units is not None:
            if isinstance(self.units, str):
                number_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.UNITS.value: self.units
                })
            elif isinstance(self.units, Widget):
                target = {"id": self.units.widget_id, "target": AttributeNames.UNITS.value}
                _widget_providers.append(target)

        if _widget_providers:
            self.add_widget_providers(number_dict, _widget_providers)

        return number_dict


class NumberInputWidget(Widget, NumberInput):
    def __init__(self,
                 title: Optional[str] = None,
                 value: Optional[Union[int, float]] = None,
                 default_value: Optional[Union[int, float]] = None,
                 placeholder: Optional[str] = None,
                 min: Optional[Union[int, float]] = None,
                 max: Optional[Union[int, float]] = None,
                 step: Optional[Union[int, float]] = None,
                 text_style: Optional[dict] = None,
                 units: Optional[str] = None,
                 **additional):
        # TODO: Should fail if text_style contains weird keys
        if text_style:
            text_style: TextStyle = text_style
        Widget.__init__(self, NumberInput.__name__,
                        compatibility=tuple([int.__name__, float.__name__, NumberInput.__name__]),
                        **additional)
        NumberInput.__init__(self, title=title, value=value, default_value=default_value, placeholder=placeholder,
                             min=min, max=max, step=step, text_style=text_style, units=units)
        self._parent_class = NumberInput.__name__

    def to_dict_widget(self):
        number_dict = Widget.to_dict_widget(self)
        number_dict = NumberInput.to_dict_widget(self, number_dict)
        return number_dict
