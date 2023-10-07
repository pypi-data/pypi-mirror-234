from __future__ import annotations

import calendar
import numpy as np
import pandas as pd
import time
import uuid
import warnings

from dataclasses import dataclass, field
from datetime import date, datetime

from typing import List, Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget
from ..util import _to_utf64_arrow_buffer, _write_arrow_file
from ....svr import AxisInfo, get_service, ISequenceService, SequenceProfile, VisualizationInfo, server_or_client
from .... import DataSet
from ....svr.sequence.sequencerepo import insert_sequence, update_levels_info
from ....svr.sequence.sequenceservice import levels_full_fn
from ....svr.db import transaction


@dataclass
class View:
    """
    Highlight a section of a Linechart.
    """
    start: Optional[Union[int, str, datetime]] = None
    end: Optional[Union[int, str, datetime]] = None

    def _adjust_view_type(self):
        """
        View values come in different types. Adjust those values to a common type so the UI can plot them.
        """
        if isinstance(self.start, datetime):
            # We need nanoseconds
            try:
                # Might fail in Windows
                self.start = int(self.start.timestamp() * 10 ** 9)
            except:
                self.start = calendar.timegm(self.start.timetuple()) * 10 ** 9
        elif isinstance(self.start, date):
            self.start = int(time.mktime(self.start.timetuple()) * 10 ** 9)
        elif isinstance(self.start, str):
            self.start = int(datetime.strptime(self.start, '%Y-%m-%d').timestamp() * 10 ** 9)

        if isinstance(self.end, datetime):
            try:
                # Might fail in Windows
                self.end = int(self.end.timestamp() * 10 ** 9)
            except:
                self.end = calendar.timegm(self.end.timetuple()) * 10 ** 9
        elif isinstance(self.end, date):
            self.end = int(time.mktime(self.end.timetuple()) * 10 ** 9)
        elif isinstance(self.end, str):
            self.end = int(datetime.strptime(self.end, '%Y-%m-%d').timestamp() * 10 ** 9)

    def to_dict(self):
        self._adjust_view_type()
        return {
            AttributeNames.BEGIN.value: str(self.start),
            AttributeNames.END.value: str(self.end)
        }


LineChartValueType = Union[
    List[int],
    List[float],
    List[str],
    np.ndarray,
    pd.DataFrame,
    pd.Series,
    DataSet
]


@dataclass
class LineChart(StateControl):
    """
    Creates a Line Chart figure. It represents either a Sequence or X and Y axis.

    .. note::
        If you need a time index in the Line Chart, your dataset must have a column called `index` with dates. 


    Parameters
    ----------
    data : DataSet, List[int], List[float], List[str], np.ndarray, pd.DataFrame or pd.Series, optional
        data to be represented.

    title : str, optional
        String with the Line Chart title. It will be placed on top of the Line Chart.

    views : List[Views], optional
        Views to be represented inside the Line Chart.

    temporal_context : TemporalContext, optional
        Temporal Context which the Line Chart is attached to.

    filtering_context : FilteringContext, optional
        Filtering Context which the Line Chart is attached to.

    multi_line_chart : bool, optional
        Try to plot multiple lines. (default True)

    multi_lane : bool, optional
        Plot one chart per lane. (default True)

    Returns
    -------
    LineChart

    Examples
    --------
    You can create a line chart using this:

    >>> line_chart = app.line_chart(title="Linechart", data=df)

    .. image:: /_static/linechart_img/linechart_default.png
        :alt: Data App main page

    By default `multi_lane=True`, so if your dataframe have more than one time series will plot in a separated lanes. You can set it to `False` you can get a line chart with only one line.

    >>> line_chart = app.line_chart(title="Linechart", data=df, multi_lane=False)

    .. image:: /_static/linechart_img/linechart_multilane_false.png
        :alt: Data App main page

    You can create a line chart or multiline chart using numpy using `plot()`.

    >>> # Numpy Arrays
    >>> x_axis = np.array([10, 20, 30, 40, 50, 55, 60, 75, 80, 95])
    >>> y_axis = np.array([10, 21, 34, 12, 14, -1, 15, 28, -5, 39])
    >>> y_axis2 = np.array([43, 21, 23, -10, 2, 15, 38, 30, -30, 12])
    >>> y_axis3 = np.array([13, 22, 15, -5, 2, 5, 18, 25, -20, 12])
    >>>
    >>> line_chart = app.line_chart(title="Multi linechart from numpy")
    >>> 
    >>> line_chart.plot(y_axis, x_axis=x_axis, label="Line 1", lane_index=0)
    >>> line_chart.plot(y_axis2, label="Line 2", lane_index=1)
    >>> line_chart.plot(y_axis3, label="Line 3", lane_index=2)

    .. image:: /_static/linechart_img/np_multilinechart.png
        :alt: Data App main page

    .. rubric:: Bind compatibility

    You can bind this widget with this: 

    .. hlist::
        :columns: 1

        * :func:`~shapelets.apps.DataApp.line_chart`

    .. rubric:: Bindable as

    You can bind this widget as: 

    *Currently this widget cannot be used as input in a binding function.*                
    """

    data: Optional[LineChartValueType] = None
    title: Optional[str] = None
    views: Optional[List[View]] = field(default_factory=lambda: [])
    # temporal_context: Optional[TemporalContext] = None
    # filtering_context: Optional[FilteringContext] = None
    multi_line_chart: Optional[bool] = True
    multi_lane: Optional[bool] = True
    _plots: List = field(default_factory=lambda: [])
    _is_type = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())
        # A subtype to differentiate between sequences or y_axis/x_axis. Requested by UI.
        self.linechart_sub_type = None
        self.sequence = None
        self.y_axis = None
        self.x_axis = None
        self._check_data()

        # Adjust Views
        if len(self.views) > 0:
            for index, view in enumerate(self.views):
                self.views[index] = self._adjust_views(view)

    def _check_data(self):
        """
        Check data inside linechart and adjust plots
        """
        if isinstance(self.data, List):
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            self.y_axis = self.data
        elif isinstance(self.data, np.ndarray):
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            self.y_axis = self.data
        elif isinstance(self.data, pd.Series) and self.data.apply(lambda x: pd.to_numeric(x, errors='coerce')).notna().all():
            self.linechart_sub_type = f"Sequence"
            self._plot_dataframe(data=self.data.to_frame())
        elif isinstance(self.data, pd.DataFrame):
            self.linechart_sub_type = f"Sequence"
            df_clean = self.data[~self.data.index.duplicated()]
            self._plot_dataframe(data=df_clean)
        elif isinstance(self.data, DataSet):
            # TODO: instead of to_pandas(), we should use to_arrow_table()
            self.linechart_sub_type = f"Sequence"
            if 'index' in self.data.columns:
                df_from_dataset = self.data.sort_by('index').to_pandas()
                df_from_dataset.set_index('index', inplace=True)
                df_from_dataset = df_from_dataset[~df_from_dataset.index.duplicated()]
            else:
                df_from_dataset = self.data.to_pandas()
                df_from_dataset.drop_duplicates(inplace=True)
            # TODO: Check plotting index and intervals.
            # if True in df_from_dataset.index.duplicated():
            #     raise Exception("Duplicates found in index")
            # if not df_from_dataset.index.is_interval():
            #     raise Exception("Index does not holds Interval")

            self._plot_dataframe(data=df_from_dataset)
        elif self.data is None:
            self.linechart_sub_type = "Empty"

    @staticmethod
    def _extract_starts_and_every_from_index(dataframe: pd.DataFrame) -> Tuple[int, int, int, bool]:
        """
        Returns start and end of the index, distance between points, and in case distances between points are not equal,
        return a flag with the need of doing a resampling.
        """
        indices = dataframe.index.values
        # The timestamp is stored as nanoseconds from epoch. Get it as an int64 and convert it to ms
        starts = int(indices[0].astype('uint64') / 1e6)
        # Check if all differences are equal
        differences = np.diff(indices)
        same_distance = np.all(differences == differences[0])
        if not same_distance:
            # Calculate the min every to know the smallest gap between points.
            all_every = [int((indices[i + 1] - indices[i]).astype("timedelta64[ms]") / np.timedelta64(1, 'ms')) for i in
                         range(0, len(indices) - 1)]
            min_every = min(all_every)
            resampling = True
        else:
            # Same distance between points, pick first
            min_every = int((indices[1] - indices[0]).astype("timedelta64[ms]") / np.timedelta64(1, 'ms'))
            resampling = False
        ends = int(indices[-1].astype('uint64') / 1e6)
        return starts, min_every, ends, resampling

    def _plot_dataframe(self, data: pd.DataFrame):
        # Are we in server or client
        server = server_or_client()
        sequence_svc = None
        if not server:
            # client executing, get server
            sequence_svc = get_service(ISequenceService)
        df_clean = data.select_dtypes(include=np.number)
        df_clean.dropna(inplace=True, axis=1, how="all")
        if not self.multi_line_chart:
            df_clean = df_clean.iloc[:, [0]]

        cols = df_clean.columns
        if len(cols) > 1:
            for col in cols:
                new_df = df_clean[col]
                self._creation(new_df, col, sequence_svc, server)
        else:
            self._creation(df_clean, cols[0], sequence_svc, server)
    @staticmethod
    def resample_chunk(chunk):
        return chunk.asfreq(pd.DateOffset(milliseconds=1000), method='ffill')

    def _creation(self,
                  df_clean: Union[pd.DataFrame, pd.Series],
                  name: str = None,
                  sequence_svc: ISequenceService = None,
                  server: bool = None):
        if isinstance(df_clean.index, pd.DatetimeIndex):
            starts, every, ends, resampling = self._extract_starts_and_every_from_index(df_clean)
            if resampling:
                # Since we get the smallest every, ffill the dataframe to match the points.
                df_clean = df_clean.asfreq(pd.DateOffset(milliseconds=every), method='ffill')
            df_clean.reset_index(drop=True)
            axis_type = "utc"
        elif isinstance(df_clean.index, pd.RangeIndex):
            starts = df_clean.index.start
            every = df_clean.index.step
            ends = starts + every * len(df_clean.index)
            df_clean.reset_index(drop=True)
            axis_type = "linear"
        else:
            warnings.warn("Could not interpret index. Reindexing data.")
            df_clean.reset_index(inplace=True, drop=True)
            starts = df_clean.index.start
            every = df_clean.index.step
            ends = starts + every * len(df_clean.index)
            axis_type = "linear"


        seq_id = str(uuid.uuid1())

        chunk_size = 256 * every
        sequence = self.create_sequence(seq_id, name, starts, every, ends, axis_type, None, chunk_size,
                                        len(df_clean.index), sequence_svc)

        self.save_arrow_file(df_clean, sequence.id)
        if not server:
            # Send request to generate levels
            sequence_svc.generate_levels(seq_id)
        else:
            # Server executing, call the function straight forward
            levels, levels_count_ser = levels_full_fn(seq_id, starts, every)
            with transaction() as conn:
                update_levels_info(seq_id, len(levels), levels_count_ser, conn)

        self._plots.append({
            AttributeNames.SEQUENCE_ID.value: sequence.id,
            AttributeNames.START.value: starts,
            AttributeNames.EVERY.value: every,
            AttributeNames.LENGTH.value: len(df_clean.index),
            AttributeNames.AXIS_TYPE.value: axis_type,
        })

    def create_sequence(self,
                        seq_id: str,
                        name: str,
                        starts: int,
                        every: int,
                        ends: int,
                        axis_type: str,
                        number_of_levels: int,
                        chunk_size: int,
                        length: int,
                        sequence_svc: ISequenceService) -> SequenceProfile:
        visual = VisualizationInfo(numberOfLevels=number_of_levels, chunkSize=chunk_size)
        axis = AxisInfo(starts=starts, every=every, ends=ends, type=axis_type)
        sequence = SequenceProfile(id=seq_id, name=name, length=length, axisInfo=axis, visualizationInfo=visual)
        # Save sequence ID, so we can keep track of the files.
        if hasattr(self, "parent_data_app") and self.parent_data_app is not None:
            self.parent_data_app._data.append(seq_id)
            self.parent_data_app._data.append(f"{seq_id}-levels")
        if sequence_svc is not None:
            # Client executing
            sequence_svc.create_sequence(sequence)
        else:
            # from Server
            with transaction() as conn:
                insert_sequence(sequence, conn)
        return sequence

    @staticmethod
    def save_arrow_file(data: pd.DataFrame, sequence_id: str):
        _write_arrow_file(data=data, uid=sequence_id, preserve_index=False)

    def replace_widget(self, new_widget: LineChart):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.data = new_widget.data
        self._check_data()
        self.title = new_widget.title
        self.views = new_widget.views
        self.temporal_context = new_widget.temporal_context
        self.filtering_context = new_widget.filtering_context
        self.multi_line_chart = new_widget.multi_line_chart
        self.multi_lane = new_widget.multi_lane
        self.linechart_sub_type = new_widget.linechart_sub_type
        self._plots = new_widget._plots
        self._is_type = new_widget._is_type

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.data is not None:
            return self.data
        return None

    def from_views(self, views: List[View]) -> LineChart:
        self.views = views
        return self

    def from_view(self, view: View) -> LineChart:
        self.views.append(view)
        return self

    def to_views(self) -> List[View]:
        return self.views

    def from_dataframe(self, dataframe: pd.DataFrame) -> LineChart:
        # TODO: save dataframe/transform
        self.data = dataframe
        return self

    def to_dataframe(self) -> pd.DataFrame:
        # TODO: transform sequence to dataframe
        return self.sequence

    def from_ndarray(self, ndarray: np.ndarray) -> LineChart:
        # TODO: save ndarray/transform
        self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
        self.data = ndarray
        return self

    def to_ndarray(self) -> np.ndarray:
        # TODO: transform sequence to ndarray
        return self.sequence

    def from_series(self, series: pd.Series):
        self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
        self.data = series

    def to_series(self) -> np.ndarray:
        # TODO: transform sequence to Series
        return self.data

    def from_list(self, lst: list) -> LineChart:
        self.linechart_sub_type = f"{LineChart.__name__}"
        self.data = lst
        return self

    def to_list(self) -> pd.DataFrame:
        return self.y_axis

    def plot(self,
             y_axis: Union[List[int], List[float], np.ndarray, pd.Series] = None,
             x_axis: Union[List[int], List[float], List[str], np.ndarray] = None,
             # sequence: Union[List[Sequence], Sequence] = None,
             label: str = None,
             lane_index: int = 0):
        # TODO: I want to complety modify or remove this function. Doesn't make sense to have a function with some many
        # isInstances once we are already checking that in previous functions.
        plot_dict = {}

        plot_dict.update({AttributeNames.LANE_INDEX.value: lane_index})

        # Handle arrays: y-axis
        # TODO: save array and send ID
        if y_axis is not None:
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            if isinstance(y_axis, np.ndarray):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis.tolist()})
            elif isinstance(y_axis, List):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis})
            elif isinstance(y_axis, pd.Series):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis.values.tolist()})

        # Handle arrays: x-axis
        # TODO: save array and send ID
        if x_axis is not None:
            if isinstance(x_axis, np.ndarray):
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis.tolist()})
            elif isinstance(x_axis, List):
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis})
            elif isinstance(x_axis, pd.Series):
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis.values.tolist()})

        if label is not None:
            # if sequence:
            #     plot_dict.update({AttributeNames.LABEL.value: sequence})
            if isinstance(label, str):
                plot_dict.update({
                    AttributeNames.LABEL.value: label
                })
        # if self.sequence is None:
        self._plots.append(plot_dict)

    def to_dict_widget(self, line_chart_dict: dict = None):
        if line_chart_dict is None:
            line_chart_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: LineChart.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        if self.title is not None:
            if isinstance(self.title, str):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.views:
            if isinstance(self.views, List) and all(isinstance(view, View) for view in self.views):
                view_list = [view.to_dict() for view in self.views]
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: view_list
                })
            elif isinstance(self.views, List):
                # For now, try to get begin and end
                view_list = [{
                    AttributeNames.BEGIN.value: str(view[0]),
                    AttributeNames.END.value: str(view[1])
                } for view in self.views]
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: view_list
                })

        if len(self._plots) > 0:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLOTS.value: self._plots
            })

        if self.linechart_sub_type:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TYPE.value: self.linechart_sub_type
            })

        if self.multi_lane is not None:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.MULTI_LANE.value: self.multi_lane
            })

        return line_chart_dict

    @staticmethod
    def to_utf64_arrow_buffer(data: pd.DataFrame) -> str:
        return _to_utf64_arrow_buffer(data=data, preserve_index=False)

    def _adjust_views(self, view) -> View:
        """
        Views can be created with integers. When a view receives integers, the start and end indicate the index of the dataframe.
        param view: View to adjust.
        returns same View if modification is not needed, or a modified View with the correct index from the dataframe as start and end.
        """
        if isinstance(view.start, int) and isinstance(view.end, int):
            view.start = self.data.index[view.start]
            view.end = self.data.index[view.end]
        return view


class LineChartWidget(Widget, LineChart):
    def __init__(self,
                 data: Optional[LineChartValueType] = None,
                 title: Optional[str] = None,
                 views: Optional[List[View]] = [],
                 # temporal_context: Optional[TemporalContext] = None,
                 # filtering_context: Optional[FilteringContext] = None,
                 multi_line_chart: Optional[bool] = True,
                 multi_lane: Optional[bool] = True,
                 **additional):
        # define TYPE
        widget_type = LineChart.__name__
        Widget.__init__(self, widget_type,
                        compatibility=tuple(
                            [str.__name__, int.__name__, float.__name__, LineChart.__name__,
                             View.__name__, "List[View]", "List[Sequence]", pd.DataFrame.__name__,
                             list.__name__, np.ndarray.__name__, pd.Series.__name__]),
                        **additional)
        LineChart.__init__(
            self,
            data=data,
            title=title,
            views=views,
            # temporal_context=temporal_context,
            # filtering_context=filtering_context,
            multi_line_chart=multi_line_chart,
            multi_lane=multi_lane
        )
        self._parent_class = LineChart.__name__

        # temporal_context_id = None
        # if self.temporal_context:
        #     temporal_context_id = self.temporal_context.context_id
        #     self.temporal_context.widgets.append(self.widget_id)
        # filtering_context_id = None
        # if self.filtering_context:
        #     filtering_context_id = filtering_context.context_id
        #     filtering_context.output_widgets.append(self.widget_id)
        # self.temporal_context = temporal_context_id
        # self.filtering_context = filtering_context_id

    def to_dict_widget(self):
        line_chart_dict = Widget.to_dict_widget(self)
        line_chart_dict = LineChart.to_dict_widget(self, line_chart_dict)
        return line_chart_dict
