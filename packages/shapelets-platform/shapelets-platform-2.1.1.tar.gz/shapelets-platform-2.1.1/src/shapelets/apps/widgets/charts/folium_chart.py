import uuid
from dataclasses import dataclass
from typing import Optional, Tuple
from folium.folium import Map
from ..widget import Widget, AttributeNames, StateControl


@dataclass
class FoliumChart(StateControl):
    """
    Creates a Folium map: a declarative statistical visualization library for Python
    (https://python-visualization.github.io/folium/quickstart.html)

    Parameters
    ----------
    title : str, optional
        String with the Folium Chart title. It will be placed on top of the Chart.

    folium_map : any, optional
        Folium map object.

    Returns
    -------
    FoliumChartWidget

    Examples
    --------     
    >>> m = folium.Map(location=[45.5236, -122.6750])
    >>> folium_chart = app.folium_chart(title='Folium Map', folium=m) 


    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * :func:`~shapelets.apps.DataApp.folium_chart`

    .. rubric:: Bindable as

    You can bind this widget as: 

    *Currently this widget cannot be used as input in a binding function.*              
    """

    title: Optional[str] = None
    folium: any = None

    def to_dict_widget(self, folium_dict: dict = None):
        if folium_dict is None:
            folium_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: FoliumChart.__name__,
                AttributeNames.PROPERTIES.value: {}
            }

        if (self.title is not None):
            folium_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TITLE.value: self.title
            })

        if (self.folium is not None):
            if isinstance(self.folium, Map):
                folium_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.folium._repr_html_()
                })

        return folium_dict


class FoliumChartWidget(Widget, FoliumChart):

    def __init__(self,
                 title: Optional[str] = None,
                 folium: Optional[any] = None,
                 **additional
                 ):
        Widget.__init__(self, 'FoliumChart',
                        compatibility=tuple([FoliumChart.__name__, ]),
                        **additional)
        FoliumChart.__init__(self, title=title, folium=folium)
        self._parent_class = FoliumChart.__name__

    def to_dict_widget(self):
        folium_dict = Widget.to_dict_widget(self)
        folium_dict = FoliumChart.to_dict_widget(self, folium_dict)

        return folium_dict
