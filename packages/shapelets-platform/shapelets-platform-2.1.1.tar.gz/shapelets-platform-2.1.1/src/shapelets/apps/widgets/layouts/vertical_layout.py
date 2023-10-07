from __future__ import annotations

import uuid

from dataclasses import dataclass, field
from typing import List, Optional
from typing_extensions import Literal

from ..widget import Widget, AttributeNames
from .panel import PanelWidget, Panel


@dataclass
class VerticalLayout(Panel):
    """
    Creates a layout that holds widget inside it vertically (stacked on-top of one another).

    Parameters
    ----------
    title : str, optional
        String with the Panel title. It will be placed on top of the Panel.

    panel_id : str, optional
        Panel ID.

    vertical_align: str, optional
        Select how widgets are align vertically: start, center, end. Default: start.

    Returns
    -------
    VerticalLayout.

    Examples
    --------
    >>> vl = app.vertical_layout()
    >>> # Create buttons and place multiple text inputs in the vertical layout
    >>> txt1 = app.text_input("Text input #1")
    >>> vl.place(txt1)         


    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * :func:`~shapelets.apps.DataApp.vertical_layout`

    .. rubric:: Bindable as

    You can bind this widget as: 

    *Currently this widget cannot be used as input in a binding function.*     
    """
    placements: dict = field(default_factory=lambda: {})
    vertical_align: Literal["start", "center", "end"] = "start"

    def place(self, widget: Widget, width: Optional[float] = None, offset: Optional[int] = None):
        """
        Place widget inside layout
        param widget: widget to place.
        param width: understood as a percentage.
        param offset: distance with the next widget.
        """
        if width is not None and width > 100:
            raise Exception("Width cannot be over a 100")
        self.widgets.append(widget)
        self.placements[widget.widget_id] = (width, offset)

    def to_dict_widget(self):
        panel_dict = {
            AttributeNames.ID.value: self.panel_id if self.panel_title else str(uuid.uuid1()),
            AttributeNames.TYPE.value: VerticalLayout.__name__,
            AttributeNames.DRAGGABLE.value: self.draggable,
            AttributeNames.RESIZABLE.value: self.resizable,
            AttributeNames.DISABLED.value: self.disabled,
            AttributeNames.PROPERTIES.value: {}
        }
        if self.panel_title is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                "panel_title": self.panel_title
            })

        if self.placements is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLACEMENTS.value: [{
                    AttributeNames.WIDGET_REF.value: key,
                    AttributeNames.WIDTH.value: width,
                    AttributeNames.OFFSET.value: offset
                } for key, (width, offset) in self.placements.items()]
            })

        if self.widgets is not None:
            widgets = [widget.to_dict_widget() for widget in self.widgets]
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.WIDGETS.value: widgets
            })

        if self.vertical_align is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VERTICAL_ALIGN.value: self.vertical_align
            })
        return panel_dict


class VerticalLayoutWidget(PanelWidget):
    """
    Creates a layout that holds widget inside it vertically (stacked on-top of one another).
    """

    def __init__(self,
                 panel_title: Optional[str] = None,
                 panel_id: Optional[str] = None,
                 vertical_align: Optional[Literal["start", "center", "end"]] = "start",
                 span: Optional[int] = None,
                 offset: Optional[int] = None,
                 **additional):
        self._parent_class = VerticalLayout.__name__
        super().__init__(panel_title, panel_id,
                         compatibility=tuple([list.__name__, List._name, VerticalLayout.__name__]),
                         **additional)
        self.span = span
        self.offset = offset
        self.vertical_align = vertical_align
        self.placements = dict()

    def replace_widget(self, new_widget: VerticalLayoutWidget):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.panel_title = new_widget.panel_title
        self.vertical_align = new_widget.vertical_align
        self.span = new_widget.span
        self.offset = new_widget.offset
        self.widgets = new_widget.widgets
        self.placements = new_widget.placements

    def place(self, widget: Widget, width: Optional[float] = None, offset: Optional[int] = None):
        """
        Place widget inside layout
        param widget: widget to place.
        param width: understood as a percentage.
        param offset: distance with the next widget.
        """
        if width is not None and width > 100:
            raise Exception("Width cannot be over a 100")
        super()._place(widget)
        self.placements[widget.widget_id] = (width, offset)

    def to_dict_widget(self):
        panel_dict = super().to_dict_widget()
        panel_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.PLACEMENTS.value: [{
                AttributeNames.WIDGET_REF.value: key,
                AttributeNames.WIDTH.value: width,
                AttributeNames.OFFSET.value: offset
            } for key, (width, offset) in self.placements.items()]
        })
        panel_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.VERTICAL_ALIGN.value: self.vertical_align
        })

        if self.span is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.COL_SPAN.value: self.span
            })

        if self.offset is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.COL_OFFSET.value: self.offset
            })
        return panel_dict
