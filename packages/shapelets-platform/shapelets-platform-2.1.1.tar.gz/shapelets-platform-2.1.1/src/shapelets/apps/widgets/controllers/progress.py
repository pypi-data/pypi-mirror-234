from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import List, Optional, Union
from typing_extensions import Literal

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Progress(StateControl):
    value: Optional[Union[str, int, float]] = None
    title: Optional[str] = None
    type: Optional[Literal["line", "circle", "dashboard"]] = None
    size: Optional[Union[int, Literal["small", "regular"]]] = None
    status: Optional[Literal["success", "exception", "normal", "active"]] = None
    stroke_color: Optional[Union[str, List[str], Literal["shapelets"]]] = None
    stroke_width: Optional[int] = None
    show_info: Optional[bool] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Progress):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.value = new_widget.value
        self.title = new_widget.title
        self.type = new_widget.type
        self.size = new_widget.size
        self.status = new_widget.status
        self.stroke_color = new_widget.stroke_color
        self.stroke_width = new_widget.stroke_width
        self.show_info = new_widget.show_info

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        return None

    def from_string(self, number: str) -> Progress:
        self.value = number
        return self

    def to_string(self) -> str:
        return str(self.value)

    def from_int(self, number: int) -> Progress:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> Progress:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    def to_dict_widget(self, progress_dict: dict = None):
        if progress_dict is None:
            progress_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Progress.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.value is not None:
            if isinstance(self.value, (str, int, float)):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value,
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value should be string, int, float or another widget")

        if self.title is not None:
            if isinstance(self.title, str):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.type is not None:
            if isinstance(self.type, str):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TYPE.value: self.type
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Type should be string")

        if self.size is not None:
            if isinstance(self.size, (str, int)):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.SIZE.value: self.size
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Size should be int or string")

        if self.status is not None:
            if isinstance(self.status, str):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.STATUS.value: self.status
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Status should be string")

        if self.stroke_color is not None:
            if isinstance(self.stroke_color, str):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.STROKE_COLOR.value: self.stroke_color
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Stroke Color should be string")

        if self.stroke_width is not None:
            if isinstance(self.stroke_width, int):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.STROKE_WIDTH.value: self.stroke_width
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Stroke Width should be int")

        if self.show_info is not None:
            if isinstance(self.show_info, bool):
                progress_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.SHOW_INFO.value: self.show_info
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Show Info should be boolean")

        if _widget_providers:
            self.add_widget_providers(progress_dict, _widget_providers)

        return progress_dict


class ProgressWidget(Progress, Widget):

    def __init__(self,
                 value: Optional[Union[str, int, float]] = None,
                 title: Optional[str] = None,
                 type: Optional[Literal["line", "circle", "dashboard"]] = None,
                 size: Optional[Union[int, Literal["small", "regular"]]] = None,
                 status: Optional[Literal["success", "exception", "normal", "active"]] = None,
                 stroke_color: Optional[Union[str, List[str], Literal["shapelets"]]] = None,
                 stroke_width: Optional[int] = None,
                 show_info: Optional[bool] = None,
                 **additional):
        Widget.__init__(self, Progress.__name__,
                        compatibility=[Progress.__name__, int.__name__, float.__name__],
                        **additional)
        Progress.__init__(self, value=value, title=title, type=type, size=size, status=status,
                          stroke_color=stroke_color, stroke_width=stroke_width, show_info=show_info)
        self._parent_class = Progress.__name__

    def to_dict_widget(self):
        progress_dict = Widget.to_dict_widget(self)
        progress_dict = Progress.to_dict_widget(self, progress_dict)
        return progress_dict
