from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Optional, Tuple

from ..widget import AttributeNames, Widget, StateControl


@dataclass
class Checkbox(StateControl):
    """
    Creates a Checkbox.

    Parameters
    ----------
    title : str, optional
        Text associated to the checkbox.

    checked : bool, optional
        Param to indicate the status of the widget

    toggle : bool, optional
        Param to display the widget as a toggle button

    Returns
    -------
    Checkbox.

    Examples
    --------
    >>> control = app.checkbox(title='Option', toggle=True)

    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * bool
        * :func:`~shapelets.apps.DataApp.checkbox`

    .. rubric:: Bindable as 

    You can bind this widget as: 

    .. hlist::
        :columns: 1

        * bool
        
    """

    title: Optional[str] = None
    checked: Optional[bool] = False
    toggle: Optional[bool] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Checkbox):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.checked = new_widget.checked
        self.toggle = new_widget.toggle

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.checked is not None:
            return self.checked
        return None

    def to_bool(self) -> bool:
        return self.checked

    def from_bool(self, new_value: bool) -> Checkbox:
        self.checked = new_value
        return self

    def to_dict_widget(self, checkbox_dict: dict = None):
        if checkbox_dict is None:
            checkbox_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Checkbox.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                checkbox_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.checked is not None:
            if isinstance(self.checked, bool):
                checkbox_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.checked
                })
            else:
                raise ValueError(f"Unexpected type {type(self.checked)} in checked")

        if self.toggle is not None:
            if isinstance(self.toggle, bool):
                checkbox_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TOGGLE.value: self.toggle
                })
            else:
                raise ValueError(f"Unexpected type {type(self.toggle)} in toggle")

        if _widget_providers:
            self.add_widget_providers(checkbox_dict, _widget_providers)

        return checkbox_dict


class CheckboxWidget(Widget, Checkbox):

    def __init__(self,
                 title: Optional[str] = None,
                 checked: Optional[bool] = False,
                 toggle: Optional[bool] = None,
                 **additional
                 ):
        Widget.__init__(self, Checkbox.__name__,
                        compatibility=tuple([Checkbox.__name__, bool.__name__]),
                        **additional)
        Checkbox.__init__(self, title=title, checked=checked, toggle=toggle)
        self._parent_class = Checkbox.__name__

    def to_dict_widget(self):
        checkbox_dict = Widget.to_dict_widget(self)
        checkbox_dict = Checkbox.to_dict_widget(self, checkbox_dict)
        return checkbox_dict
