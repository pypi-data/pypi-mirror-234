from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Tuple, Optional, Union

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class TextInput(StateControl):
    """
    A basic widget for getting the user input as a text field.

    Parameters
    ----------
    title : str, optional
        String with the widget title. It will be placed on top of the widget box.

    value : str, int or float, optional
        Default value.

    placeholder : str, optional
        Text showed inside the widget by default.

    multiline : bool, optional
        Show text in multiline.

    text_style : dict, optional
        Dict to customize text: font size, font type y font style.

    toolbar : bool, optional
        Show toolbar on top of the widget.

    width : int or float, optional
        width of the text input. It represents a percentage value.

    markdown : bool, optional
        Flag to indicate if markdown format in in input text.

    Returns
    -------
    Text Input.

    Examples
    --------
    >>> text_input = app.text_input() 

    >>> text_input = app.text_input(title="Find object",placeholder="Write here", markdown=True)

    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * str
        * int
        * :func:`~shapelets.apps.DataApp.text_input`


    .. rubric:: Bindable as

    You can bind this widget as: 

    .. hlist::
        :columns: 1

        * str
        * int
    """
    value: Optional[Union[str, int, float]] = None
    title: Optional[str] = None
    text_style: Optional[dict] = None
    markdown: Optional[bool] = None
    placeholder: Optional[str] = None
    multiline: Optional[bool] = None
    toolbar: Optional[bool] = None
    width: Optional[Union[int, float]] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: TextInput):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.value = new_widget.value
        self.title = new_widget.title
        self.text_style = new_widget.text_style
        self.markdown = new_widget.markdown
        self.placeholder = new_widget.placeholder
        self.multiline = new_widget.multiline
        self.toolbar = new_widget.toolbar
        self.width = new_widget.width

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        return None

    def from_string(self, string: str) -> TextInput:
        self.value = string
        return self

    def to_string(self) -> str:
        return str(self.value)

    def from_int(self, number: int) -> TextInput:
        self.value = number
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> TextInput:
        self.value = number
        return self

    def to_float(self) -> float:
        return float(self.value)

    def to_dict_widget(self, text_input_dict: dict = None):
        if text_input_dict is None:
            text_input_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: TextInput.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.value is not None:
            if isinstance(self.value, (str, int, float)):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
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
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.text_style is not None:
            if isinstance(self.text_style, dict):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT_STYLE.value: self.text_style
                })

        if self.markdown is not None:
            if isinstance(self.markdown, bool):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MARKDOWN.value: self.markdown
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Markdown should be boolean")

        if self.placeholder is not None:
            if isinstance(self.placeholder, str):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.PLACEHOLDER.value: self.placeholder
                })
            elif isinstance(self.placeholder, Widget):
                target = {"id": self.placeholder.widget_id, "target": AttributeNames.PLACEHOLDER.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Placeholder should be a string or another widget")

        if self.multiline is not None:
            if isinstance(self.multiline, bool):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MULTI_LINE.value: self.multiline
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Multiline value should be a boolean")

        if self.toolbar is not None:
            if isinstance(self.multiline, bool):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TOOLBAR.value: self.toolbar
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: toolbar value should be a boolean")

        if self.width is not None:
            if self.width > 100 or self.width < 0:
                raise ValueError("Width percentage cannot be higher than 100 or smaller than 0.")

            if isinstance(self.width, (int, float)):
                text_input_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.WIDTH.value: self.width
                })
            elif isinstance(self.width, Widget):
                target = {"id": self.width.widget_id, "target": AttributeNames.WIDTH.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Width value should be a int or float or another widget")

        if _widget_providers:
            self.add_widget_providers(text_input_dict, _widget_providers)

        return text_input_dict


class TextInputWidget(TextInput, Widget):

    def __init__(self,
                 value: Optional[Union[str, int, float]] = None,
                 title: Optional[str] = None,
                 text_style: Optional[dict] = None,
                 markdown: Optional[bool] = None,
                 placeholder: Optional[str] = None,
                 multiline: Optional[bool] = None,
                 toolbar: Optional[bool] = None,
                 width: Optional[Union[int, float]] = None,
                 **additional):
        Widget.__init__(self, TextInput.__name__,
                        compatibility=tuple([str.__name__, TextInput.__name__]),
                        **additional)
        TextInput.__init__(self, value=value, title=title, text_style=text_style, markdown=markdown,
                           placeholder=placeholder, multiline=multiline, toolbar=toolbar, width=width)
        self._parent_class = self.widget_type = TextInput.__name__

    def to_dict_widget(self):
        text_input_dict = Widget.to_dict_widget(self)
        text_input_dict = TextInput.to_dict_widget(self, text_input_dict)
        return text_input_dict
