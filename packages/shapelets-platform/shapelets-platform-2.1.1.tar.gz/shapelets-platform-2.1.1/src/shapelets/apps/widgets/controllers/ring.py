from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Optional, Union

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Ring(StateControl):
    """
    Creates a Ring.

    Parameters
    ----------
    title : str, optional
        Text associated to the Ring.

    value : int, float, optional
        Param to indicate the value of the widget as a percentage

    color : str, optional
        Color to display the widget

    Returns
    -------
    Ring.

    Examples
    --------
    >>> ring = app.ring(title='Title', value=25, color="Red")

    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * int
        * float
        * :func:`~shapelets.apps.DataApp.ring`

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
    color: Optional[str] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Ring):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.value = new_widget.value
        self.color = new_widget.color

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

    def from_int(self, new_value: int) -> Ring:
        self.value = new_value
        return self

    def to_float(self) -> float:
        return float(self.value)

    def from_float(self, new_value: float) -> Ring:
        self.value = new_value
        return self

    def to_dict_widget(self, ring_dict: dict = None):
        if ring_dict is None:
            ring_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Ring.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                ring_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.value is not None:
            if isinstance(self.value, (int, float)):
                ring_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value
                })
            else:
                raise ValueError(f"Unexpected type {type(self.value)} in value")

        if self.color is not None:
            if isinstance(self.color, str):
                ring_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.COLOR.value: self.color
                })
            else:
                raise ValueError(f"Unexpected type {type(self.color)} in color")

        if _widget_providers:
            self.add_widget_providers(ring_dict, _widget_providers)

        return ring_dict


class RingWidget(Widget, Ring):

    def __init__(self,
                 title: Optional[str] = None,
                 value: Optional[Union[int, float]] = None,
                 color: Optional[str] = None,
                 **additional
                 ):
        Widget.__init__(self, Ring.__name__,
                        compatibility=tuple([Ring.__name__, int.__name__, float.__name__]),
                        **additional)
        Ring.__init__(self, title=title, value=value, color=color)
        self._parent_class = Ring.__name__

    def to_dict_widget(self):
        ring_dict = Widget.to_dict_widget(self)
        ring_dict = Ring.to_dict_widget(self, ring_dict)
        return ring_dict
