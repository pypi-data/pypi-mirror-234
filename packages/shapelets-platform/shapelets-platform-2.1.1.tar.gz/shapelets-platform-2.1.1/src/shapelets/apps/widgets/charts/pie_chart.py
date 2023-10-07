# from typing import Union, List
#
# from ..widget import Widget, AttributeNames
# from ....model import NDArray
#
#
# class PieChart(Widget):
#     def __init__(self,
#                  data: Union[List[int], List[float], NDArray],
#                  categories: Union[List[int], List[float], List[str], NDArray] = None,
#                  name: str = None,
#                  title: str = None,
#                  **additional):
#         super().__init__(self.__class__.__name__, name, **additional)
#         if categories:
#             self.categories = categories
#         self.data = data
#         self.title = title
#
#     def to_dict_widget(self):
#         pie_chart_dict = super().to_dict_widget()
#         if hasattr(self, "categories"):
#             categories_value = None
#
#             if isinstance(self.categories, List) and all(
#                     [isinstance(item, int) or isinstance(item, float) or isinstance(item, str) for item in
#                      self.categories]):
#                 categories_value = self.categories
#
#             if isinstance(self.categories, NDArray):
#                 categories_value = self.categories.nd_array_id
#
#             pie_chart_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.CATEGORIES.value: categories_value
#             })
#
#         if hasattr(self, "data"):
#             data_value = None
#
#             if isinstance(self.data, List) and all(
#                     [isinstance(item, int) or isinstance(item, float) for item in self.data]):
#                 data_value = self.data
#
#             if isinstance(self.data, NDArray):
#                 data_value = self.data.nd_array_id
#
#             pie_chart_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.DATA.value: data_value
#             })
#
#         if self.title is not None:
#             if isinstance(self.title, str):
#                 pie_chart_dict[AttributeNames.PROPERTIES.value].update({
#                     AttributeNames.TITLE.value: self.title
#                 })
#
#         return pie_chart_dict
