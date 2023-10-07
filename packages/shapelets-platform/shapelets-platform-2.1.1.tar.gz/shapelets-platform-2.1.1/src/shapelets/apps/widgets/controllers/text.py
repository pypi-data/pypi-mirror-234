from __future__ import annotations

import datetime
import uuid

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Text(StateControl):
    """
    Creates a Label.

    Parameters
    ----------
    value : str, int or float, optional
        Text value of the widget.

    title : str, optional
        Title of the widget.

    text_style : dict, optional
        Text style for the label

    markdown : bool, optional
        Flag to indicate if Label is markdown


    Returns
    -------
    Label

    Examples
    --------
    >>> text1 = app.text("Hello world!")

    >>> text1 = app.text("# Hello world!", markdown = True)


    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * str
        * int
        * float
        * :func:`~shapelets.apps.DataApp.text`
        * datetime

    .. rubric:: Bindable as 

    You can bind this widget as: 

    .. hlist::
        :columns: 1

        * str
        * int
        * float
        * :func:`~shapelets.apps.DataApp.text`        

    """

    value: Optional[Union[str, int, float]] = None
    title: Optional[str] = None
    text_style: Optional[dict] = None
    markdown: Optional[bool] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Text):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.value = new_widget.value
        self.title = new_widget.title
        self.text_style = new_widget.text_style
        self.markdown = new_widget.markdown

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        return None

    def from_string(self, string: str) -> Text:
        self.value = string
        return self

    def to_string(self) -> str:
        return str(self.value)

    def from_int(self, number: int) -> Text:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> Text:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    def from_datetime(self, dt: datetime.datetime) -> Text:
        self.value = str(dt)
        return self

    def to_dict_widget(self, text_dict: dict = None):
        if text_dict is None:
            text_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Text.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.value is not None:
            if isinstance(self.value, (str, int, float, list)):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: str(self.value),
                })
            elif isinstance(self.value, Widget):
                target = {"id": self.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value should be string, int, float or another widget")

        if self.title is not None:
            if isinstance(self.title, str):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.text_style is not None:
            if isinstance(self.text_style, dict):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT_STYLE.value: self.text_style
                })

        if self.markdown is not None:
            if isinstance(self.markdown, bool):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MARKDOWN.value: self.markdown
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Markdown should be boolean")

        if _widget_providers:
            self.add_widget_providers(text_dict, _widget_providers)

        return text_dict


class TextWidget(Text, Widget):

    def __init__(self,
                 value: Optional[Union[str, int, float]] = None,
                 title: Optional[str] = None,
                 text_style: Optional[dict] = None,
                 markdown: Optional[bool] = False,
                 **additional):
        Widget.__init__(self, Text.__name__,
                        compatibility=tuple([str.__name__, int.__name__, float.__name__,
                                            Text.__name__, datetime.datetime.__name__]),
                        **additional)
        Text.__init__(self, value=value, title=title, text_style=text_style, markdown=markdown)
        self._parent_class = Text.__name__

    def to_dict_widget(self):
        text_dict = Widget.to_dict_widget(self)
        text_dict = Text.to_dict_widget(self, text_dict)
        return text_dict
