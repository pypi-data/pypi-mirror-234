# from typing import Union, List
# from ..widget import Widget, AttributeNames
# from ....model import NDArray
#
#
# class ScatterPlot(Widget):
#     def __init__(self,
#                  x_axis: Union[List[int], List[float], NDArray],
#                  y_axis: Union[List[int], List[float], NDArray],
#                  size: Union[List[int], List[float], NDArray] = None,
#                  color: Union[List[int], List[float], NDArray] = None,
#                  categories: Union[List[int], List[float], List[str], NDArray] = None,
#                  name: str = None,
#                  title: str = None,
#                  trend_line: bool = False,
#                  **additional):
#         super().__init__(self.__class__.__name__, name, **additional)
#         if size:
#             self.size = size
#         if color:
#             self.color = color
#         if categories:
#             self.categories = categories
#         self.x_axis = x_axis
#         self.y_axis = y_axis
#         self.title = title
#         self.trend_line = trend_line
#
#     def to_dict_widget(self):
#         scatter_plot_dict = super().to_dict_widget()
#         if hasattr(self, "size"):
#             size_value = None
#
#             if isinstance(self.size, List) and all(
#                     [isinstance(item, int) or isinstance(item, float) for item in self.size]):
#                 size_value = self.size
#
#             if isinstance(self.size, NDArray):
#                 size_value = self.size.nd_array_id
#
#             scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.SIZE.value: size_value
#             })
#         if hasattr(self, "color"):
#             color_value = None
#
#             if isinstance(self.color, List) and all(
#                     [isinstance(item, int) or isinstance(item, float) for item in self.color]):
#                 color_value = self.color
#
#             if isinstance(self.color, NDArray):
#                 color_value = self.color.nd_array_id
#
#             scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.COLOR.value: color_value
#             })
#
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
#             scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.CATEGORIES.value: categories_value
#             })
#
#         if self.title is not None:
#             if isinstance(self.title, str):
#                 scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                     AttributeNames.TITLE.value: self.title
#                 })
#
#         if hasattr(self, "x_axis"):
#             x_axis_value = None
#
#             if isinstance(self.x_axis, List) and all(
#                     [isinstance(item, int) or isinstance(item, float) for item in self.x_axis]):
#                 x_axis_value = self.x_axis
#
#             if isinstance(self.x_axis, NDArray):
#                 x_axis_value = self.x_axis.nd_array_id
#
#             scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.X_AXIS.value: x_axis_value
#             })
#
#         if hasattr(self, "y_axis"):
#             y_axis_value = None
#
#             if isinstance(self.y_axis, List) and all(
#                     [isinstance(item, int) or isinstance(item, float) for item in self.y_axis]):
#                 y_axis_value = self.y_axis
#
#             if isinstance(self.y_axis, NDArray):
#                 y_axis_value = self.y_axis.nd_array_id
#
#             scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.Y_AXIS.value: y_axis_value
#             })
#
#         if hasattr(self, "trend_line"):
#             scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.TREND_LINE.value: self.trend_line
#             })
#         return scatter_plot_dict
