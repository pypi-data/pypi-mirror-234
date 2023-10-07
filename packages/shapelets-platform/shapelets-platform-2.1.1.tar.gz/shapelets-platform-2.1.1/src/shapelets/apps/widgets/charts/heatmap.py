# from typing import Union, List
#
# from ..widget import Widget, AttributeNames
# from ....model import NDArray
#
#
# class HeatMap(Widget):
#     def __init__(self,
#                  x_axis: Union[List[int], List[float], List[str], NDArray],
#                  y_axis: Union[List[int], List[float], List[str], NDArray],
#                  z_axis: Union[List[int], List[float], NDArray],
#                  name: str = None,
#                  title: str = None,
#                  **additional):
#         super().__init__(self.__class__.__name__, name, **additional)
#         self.title = title
#         self.x_axis = x_axis
#         self.y_axis = y_axis
#         self.z_axis = z_axis
#
#     def to_dict_widget(self):
#         heatmap_dict = super().to_dict_widget()
#
#         # title
#         if isinstance(self.title, str):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.TITLE.value: self.title
#             })
#
#         def _check_types(axis):
#             print(axis)
#             if all(isinstance(element, type(axis[0])) for element in axis):
#                 return axis
#             else:
#                 raise Exception("Mixed types not supported")
#
#         # x_axis
#         if isinstance(self.x_axis, List):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.X_AXIS.value: _check_types(self.x_axis)
#             })
#
#         if isinstance(self.x_axis, NDArray):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.X_AXIS.value: self.x_axis.nd_array_id
#             })
#
#         # y_axis
#         if isinstance(self.y_axis, List):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.Y_AXIS.value: _check_types(self.y_axis)
#             })
#
#         if isinstance(self.y_axis, NDArray):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.Y_AXIS.value: self.y_axis.nd_array_id
#             })
#
#         # z_axis
#         if isinstance(self.z_axis, List):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.Z_AXIS.value: _check_types(self.z_axis)
#             })
#
#         if isinstance(self.z_axis, NDArray):
#             heatmap_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.Z_AXIS.value: self.z_axis.nd_array_id
#             })
#
#         return heatmap_dict
