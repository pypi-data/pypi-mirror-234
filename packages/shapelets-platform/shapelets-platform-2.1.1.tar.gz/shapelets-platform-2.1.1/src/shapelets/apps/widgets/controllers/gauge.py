from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Optional, Union

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Gauge(StateControl):
    """
    Creates a Gauge.

    Parameters
    ----------
    title : str, optional
        Text associated to the Gauge.

    value : int, float, optional
        Param to indicate the value of the widget. Must be between [0,1], cause 1 equals 100%. 


    Returns
    -------
    Gauge.

    Examples
    --------
    >>> gauge = app.gauge(title='Title', value=0.25)

    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * int
        * float
        * :func:`~shapelets.apps.DataApp.gauge`

    .. rubric:: Bindable as 

    You can bind this widget as: 

    .. hlist::
        :columns: 1

        * int
        * float
        * string

    """

    title: Optional[str] = None
    value: Optional[Union[int, float]] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Gauge):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.value = new_widget.value

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        return None

    def to_string(self) -> str:
        return str(self.value)

    def to_int(self) -> int:
        return int(self.value)

    def from_int(self, new_value: int) -> Gauge:
        self.value = new_value
        return self

    def to_float(self) -> float:
        return float(self.value)

    def from_float(self, new_value: float) -> Gauge:
        self.value = new_value
        return self

    def to_dict_widget(self, gauge_dict: dict = None):
        if gauge_dict is None:
            gauge_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Gauge.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                gauge_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.value is not None:
            if isinstance(self.value, (int, float)):
                gauge_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value
                })
            else:
                raise ValueError(f"Unexpected type {type(self.value)} in value")


        if _widget_providers:
            self.add_widget_providers(gauge_dict, _widget_providers)

        return gauge_dict


class GaugeWidget(Widget, Gauge):

    def __init__(self,
                 title: Optional[str] = None,
                 value: Optional[Union[int, float]] = None,
                 **additional
                 ):
        Widget.__init__(self, Gauge.__name__,
                        compatibility=tuple([Gauge.__name__, int.__name__, float.__name__]),
                        **additional)
        Gauge.__init__(self, title=title, value=value)
        self._parent_class = Gauge.__name__

    def to_dict_widget(self):
        gauge_dict = Widget.to_dict_widget(self)
        gauge_dict = Gauge.to_dict_widget(self, gauge_dict)
        return gauge_dict
