from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Optional

from ..widget import Widget, AttributeNames, StateControl


@dataclass
class AltairChart(StateControl):
    """
    Creates an Vega-Altair chart: a declarative statistical visualization library for Python
    (https://altair-viz.github.io/index.html).

    Parameters
    ----------
    title : str, optional
        String with the Altair Chart title. It will be placed on top of the Chart.

    spec : any , optional 
        Loads a JSON specification for Altair Chart.

    Returns
    -------
    AltairChartWidget

    Examples
    --------
    >>> spec = alt.Chart(source).mark_bar().encode(
    >>>     x='a',
    >>>     y='b'
    >>> ) 
    >>> altair_chart = app.altair_chart(title='Title Altair Chart', spec=spec)


    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * :func:`~shapelets.apps.DataApp.altair_chart`

    .. rubric:: Bindable as

    You can bind this widget as: 

    *Currently this widget cannot be used as input in a binding function.*        
    """
    title: Optional[str] = None
    chart: any = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: AltairChart):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.chart = new_widget.chart

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.chart is not None:
            return self.chart
        return None

    def to_dict_widget(self, alt_dict: dict = None):
        if alt_dict is None:
            alt_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: AltairChart.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }

        if self.chart is not None:
            if not hasattr(self.chart, "to_json"):
                raise Exception("You must inject an altair chart")
            if self.title is not None:
                self.chart.title = self.title
            alt_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VALUE.value: self.chart.to_json(indent=2)
            })

        return alt_dict


class AltairChartWidget(Widget, AltairChart):

    def __init__(self,
                 title: Optional[str] = None,
                 chart: Optional[any] = None,
                 **additional
                 ):
        Widget.__init__(self, 'AltairChart',
                        compatibility=tuple([AltairChart.__name__, ]),
                        **additional)
        AltairChart.__init__(self, title=title, chart=chart)
        self._parent_class = AltairChart.__name__

    def to_dict_widget(self):
        alt_dict = Widget.to_dict_widget(self)
        alt_dict = AltairChart.to_dict_widget(self, alt_dict)
        return alt_dict
