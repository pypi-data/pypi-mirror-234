from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Optional, Union
from typing_extensions import Literal

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Metric(StateControl):
    """
    Creates a Metric.

    Parameters
    ----------
    title : str, optional
        Text associated to the metric widget.

    value : str, optional
        Param to indicate the value of the widget

    unit : str, optional
        Unit of the widget

    delta : str, optional
        Delta of the metric

    align : str, optional
        Select how the metric is aligned vertically: right or left.

    Returns
    -------
    Metric.

    Examples
    --------
    >>> metric = app.metric(title='Title', value="2023,46", unit="$", delta="+20,25", align="right")

    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * str
        * int
        * float
        * :func:`~shapelets.apps.DataApp.metric`

    .. rubric:: Bindable as 

    You can bind this widget as: 

    .. hlist::
        :columns: 1

        * str
        * int
        * float

    """

    title: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    delta: Optional[str] = None
    align: Optional[Literal["right", "left"]] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Metric):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.value = new_widget.value
        self.unit = new_widget.unit
        self.delta = new_widget.delta
        self.align = new_widget.align

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        return None

    def to_string(self) -> str:
        return str(self.value)

    def from_string(self, new_value: str) -> str:
        self.value = new_value
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_int(self, new_value: int) -> Metric:
        self.value = str(new_value)
        return self

    def to_float(self) -> float:
        return float(self.value)

    def from_float(self, new_value: float) -> Metric:
        self.value = str(new_value)
        return self

    def to_dict_widget(self, metric_dict: dict = None):
        if metric_dict is None:
            metric_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Metric.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                metric_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.value is not None:
            if isinstance(self.value, str):
                metric_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value
                })
            else:
                raise ValueError(f"Unexpected type {type(self.value)} in value")

        if self.unit is not None:
            if isinstance(self.unit, str):
                metric_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.UNIT.value: self.unit
                })
            else:
                raise ValueError(f"Unexpected type {type(self.unit)} in unit")

        if self.delta is not None:
            if isinstance(self.delta, str):
                metric_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.DELTA.value: self.delta
                })
            else:
                raise ValueError(f"Unexpected type {type(self.delta)} in delta")

        if self.align is not None:
            if isinstance(self.align, str):
                metric_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.ALIGN.value: self.align
                })
            else:
                raise ValueError(f"Unexpected type {type(self.align)} in align")
        if _widget_providers:
            self.add_widget_providers(metric_dict, _widget_providers)

        return metric_dict


class MetricWidget(Widget, Metric):

    def __init__(self,
                 title: Optional[str] = None,
                 value: Optional[str] = None,
                 unit: Optional[str] = None,
                 delta: Optional[str] = None,
                 align: Optional[Literal["right", "left"]] = None,
                 **additional
                 ):
        Widget.__init__(self, Metric.__name__,
                        compatibility=tuple([Metric.__name__, str.__name__, int.__name__, float.__name__]),
                        **additional)
        Metric.__init__(self, title=title, value=value, unit=unit, delta=delta, align=align)
        self._parent_class = Metric.__name__

    def to_dict_widget(self):
        metric_dict = Widget.to_dict_widget(self)
        metric_dict = Metric.to_dict_widget(self, metric_dict)
        return metric_dict
