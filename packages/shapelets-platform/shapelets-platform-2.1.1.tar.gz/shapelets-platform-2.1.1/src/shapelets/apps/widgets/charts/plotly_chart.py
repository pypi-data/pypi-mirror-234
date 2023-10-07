# from dataclasses import dataclass
# from typing import Optional
# import plotly
# import plotly.express as px
# from ..widget import Widget, AttributeNames, StateControl


# @dataclass
# class PlotlyChart(StateControl):
#     title: Optional[str] = None
#     value: any = None


# class PlotlyChartWidget(Widget, PlotlyChart):

#     def __init__(self,
#                  title: Optional[str] = None,
#                  value: Optional[any] = None,
#                  **additional
#                  ):
#         Widget.__init__(self, 'PlotlyChart', **additional)
#         PlotlyChart.__init__(self, title, value)

#     def to_dict_widget(self):
#         chart_dict = super().to_dict_widget()

#         if (self.title is not None):
#             chart_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.TITLE.value: self.title
#             })

#         if (self.value is not None):
#             graphJSON = plotly.io.to_json(self.value, pretty=True)

#             chart_dict[AttributeNames.PROPERTIES.value].update({
#                 AttributeNames.VALUE.value: graphJSON
#             })

#         return chart_dict
