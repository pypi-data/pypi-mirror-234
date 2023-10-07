from typing import Union, List
from dataclasses import dataclass

from ..widget import Widget, AttributeNames, StateControl


@dataclass
class RadarArea(StateControl):
    categories: Union[List[int], List[float], List[str]] = None
    data: Union[List[int], List[float]] = None
    groups: Union[List[int], List[float], List[str]] = None
    name: str = None
    title: str = None


class RadarAreaWidget(Widget, RadarArea):
    def __init__(self,
                 categories: Union[List[int], List[float], List[str]],
                 data: Union[List[int], List[float]],
                 groups: Union[List[int], List[float], List[str]],
                 name: str = None,
                 title: str = None,
                 **additional):

        Widget.__init__(self, 'RadarArea', **additional)
        RadarArea.__init__(self, categories, data, groups, name, title)

        self.categories = categories
        self.data = data
        self.groups = groups
        self.title = title

    def to_dict_widget(self):
        radar_chart_dict = super().to_dict_widget()
        if self.categories is not None:
            categories_value = None
            if isinstance(self.categories, List) and all(
                    [isinstance(item, int) or isinstance(item, float) or isinstance(item, str) for item in
                     self.categories]):
                categories_value = self.categories
            # if isinstance(self.categories, NDArray):
            #     categories_value = self.categories.nd_array_id

            radar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.CATEGORIES.value: categories_value
            })
        if self.data:
            data_value = None
            if isinstance(self.data, List) and all([isinstance(item, (int, float)) for item in self.data]):
                data_value = self.data
            # if isinstance(self.data, NDArray):
            #     data_value = self.data.nd_array_id

            radar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DATA.value: data_value
            })
        if self.groups:
            groups_value = None
            if isinstance(self.groups, List) and all(
                    [isinstance(item, int) or isinstance(item, float) or isinstance(item, str) for item in
                     self.groups]):
                groups_value = self.groups
            # if isinstance(self.groups, NDArray):
            #     groups_value = self.groups.nd_array_id

            radar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.GROUPS.value: groups_value
            })
        if self.title is not None:
            if isinstance(self.title, str):
                radar_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })

        return radar_chart_dict
