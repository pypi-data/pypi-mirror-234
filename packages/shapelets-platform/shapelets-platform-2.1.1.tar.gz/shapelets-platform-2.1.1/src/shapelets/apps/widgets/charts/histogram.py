# from typing import Union, List
#
# from ..widget import Widget, AttributeNames
# from ....model import NDArray
#
#
# class Histogram(Widget):
#     def __init__(self, x: Union[List[int], List[float], NDArray],
#                  bins: Union[int, float] = None,
#                  cumulative: bool = False, **additional):
#         super().__init__(self.__class__.__name__, "Histogram", **additional)
#         self._x = x
#         self._bins = bins
#         self._cumulative = cumulative
#
#     def to_dict_widget(self):
#         histogram_dict = super().to_dict_widget()
#
#         if isinstance(self._x, List) and all([isinstance(item, int) or isinstance(item, float) for item in self._x]):
#             histogram_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.X.value: self._x
#             })
#         if isinstance(self._x, NDArray):
#             histogram_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.X.value: self._x.nd_array_id
#             })
#
#         if self._bins is not None:
#             if isinstance(self._bins, int) or isinstance(self._bins, float):
#                 histogram_dict[AttributeNames.PROPERTIES.value].update({
#                     AttributeNames.BINS.value: self._bins
#                 })
#             if isinstance(self._bins, float) or isinstance(self._bins, float):
#                 histogram_dict[AttributeNames.PROPERTIES.value].update({
#                     AttributeNames.BINS.value: self._bins
#                 })
#
#         if isinstance(self._cumulative, bool):
#             histogram_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.CUMULATIVE.value: self._cumulative
#             })
#
#         return histogram_dict
