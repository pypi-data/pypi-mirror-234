import datetime
import json
# import numpy as np
import pandas as pd
import subprocess
import sys
import time

from enum import Enum
from json import JSONEncoder
from matplotlib.figure import Figure
from pathlib import Path
from typing import List, Optional, Union, NamedTuple
from typing_extensions import Literal
from urllib.parse import urlparse

from .widgets.charts.altair_chart import AltairChartWidget
from .widgets.charts.folium_chart import FoliumChartWidget
from .widgets.charts.line_chart import LineChartWidget, LineChartValueType,View
# from .widgets.charts.plotly_chart import PlotlyChartWidget
# from .widgets.contexts.filtering_context import FilteringContext
# from .widgets.contexts.metadata_field import MetadataField
# from .widgets.contexts.temporal_context import TemporalContext
from .widgets.controllers.button import Button
from .widgets.controllers.checkbox import CheckboxWidget
from .widgets.controllers.datetime_range_selector import DatetimeRangeSelectorWidget
from .widgets.controllers.datetime_selector import DateSelectorWidget
from .widgets.controllers import GaugeWidget, MetricWidget, RingWidget
from .widgets.controllers.image import ImageWidget
# from .widgets.controllers.list import ListWidget
from .widgets.controllers.number_input import NumberInputWidget
from .widgets.controllers.progress import ProgressWidget
from .widgets.controllers.radio_group import RadioGroupWidget
from .widgets.controllers.selector import SelectorWidget
from .widgets.controllers.slider import SliderWidget
from .widgets.controllers.table import Condition, TableWidget
from .widgets.controllers.text import TextWidget
from .widgets.controllers.text_input import TextInputWidget
from .widgets.controllers.timer import TimerWidget
from .widgets.layouts.horizontal_layout import HorizontalLayoutWidget
from .widgets.layouts.panel import PanelWidget
from .widgets.layouts.tabs_layout import TabsLayoutWidget
from .widgets.layouts.vertical_layout import VerticalLayoutWidget
from .widgets.widget import Widget

from .. import DataSet
from ..svr import get_service, IDataAppsService, Settings, SignedPrincipalId, _load_alias_from_host


class AttributeNames(Enum):
    CREATION_DATE = "creationDate"
    CUSTOM_GRAPH = "customGraphs"
    DESCRIPTION = "description"
    FUNCTIONS = "functions"
    FILTERING_CONTEXTS = "filteringContexts"
    MAIN_PANEL = "mainPanel"
    NAME = "name"
    ID = "id"
    TAGS = "tags"
    TEMPORAL_CONTEXTS = "temporalContexts"
    TITLE = "title"
    UPDATE_DATE = "updateDate"
    VERSION = "version"


class Version(NamedTuple):
    major: int
    minor: int


class DataApp:
    """
    Entry point for data app registration.
    """

    @staticmethod
    def now() -> int:
        return int(time.mktime(time.gmtime()) * 1e3)

    def __init__(self,
                 name: str,  # acts as app_id, must be unique
                 description: str = None,
                 version: Version = None,
                 tags: List[str] = [],
                 main_panel: PanelWidget = None):
        """
        Initializes a dataApp.
        param name: String with the dataApp Name.
        param description: String with the dataApp Description.
        param version: dataApp version (major and minor).
        param tags: dataApp tags.
        param main_panel: dataApp Main Panel.
        """
        self.name = name
        self.description = description
        self.version = version
        self.tags = tags
        self.main_panel = main_panel if main_panel else VerticalLayoutWidget(panel_id=name)
        self.title = name
        self.temporal_contexts = []
        self.filtering_contexts = []
        self.functions = {}
        self.groups = None
        self._data = []

    def _update_data(self, data: List[str]):
        from ..svr.dataapps.dataappsrepo import _add_data, _load_dataapp_by_name_and_version
        from ..svr.db import transaction
        """
        Update data info belonging to the dataApp to keep track of what files belong to each dataApp. This allows us
        to do a correct cleaning once the dataApp is deleted.
        """
        with transaction() as conn:
           uid = _load_dataapp_by_name_and_version(self.name, self.version[0], self.version[1], conn).uid
           _add_data(uid, data, conn)

    @staticmethod
    def _initial_registration_message(dataapp_svc: IDataAppsService):
        token = dataapp_svc.session.auth.token.split("Bearer ", 1)[1]
        principal = SignedPrincipalId.from_token(token)
        url = dataapp_svc.session.prefix_url
        print("Trying to register DataApp")
        print(f"User: {principal.id}")
        print(f"Host: {url}")
        print("---------------------------------------------------------------------------------\n")

    def register(self,
                 host: Optional[str] = None,
                 user_name: Optional[str] = None,
                 groups: Optional[Union[List[str], str]] = None):
        """
        Registers the DataApp. When host or username are not provided, the default information will be used.

        Parameters
        ----------
        host : str, optional
            Alias of the host where the dataApp will be registered. In addition, user can specify the full address of the host.

        user_name : str, optional
            User registering the dataApp

        groups : List[str], str, optional
            Group/s where the dataApp will be registered.


        It checks DataApp's code to avoid possible errors during Runtime (using mypy library).
        If some error is found, it will print a message to the user but the DataApp will be registered anyway
        """
        # Load settings
        settings = get_service(Settings)
        if groups is not None:
            self.groups = groups

        if host is not None:
            full_host = urlparse(host)
            if all([full_host.scheme, full_host.netloc]) and len(full_host.netloc.split(".")) > 1:
                # url is valid
                host = str(full_host.hostname)
                current_alias = _load_alias_from_host(host)
            else:
                # Look for alias
                alias_host = settings.client.clients.get(host)
                if alias_host:
                    current_alias = host
                    host = str(alias_host.host)
                else:
                    raise ValueError(f"Server alias {host} not found.")

        else:
            # Search for default server
            current_alias = settings.client.default_server
            if current_alias is not None:
                host = str(settings.client.clients.get(current_alias).host)
            else:
                raise ValueError("Unable to find server information. Please, register a server or use the parameter 'host' to provide with the needed information")

        if user_name is None:
            # get default user
            user_name = settings.client.clients.get(current_alias).default_user
            if user_name is None:
                raise ValueError("Username was not provided and not deafult information about user was found in the configuration.")


        dataapp_svc = get_service(IDataAppsService, host, user_name)
        self._initial_registration_message(dataapp_svc)
        response = dataapp_svc.create(self)

        try:
            self._check_dataapp()

        except FileNotFoundError as exc:
            print(f"Process failed because the executable could not be found.\n{exc}")
            print(f"DataApp {self.name} has been registered but static type checker program couldn't be validated. \n")

        except subprocess.CalledProcessError as exc:
            print(f"Process failed because did not return a successful return code. ")
            print(f"Returned {exc.returncode}\n{exc}")
            print(f"DataApp {self.name}  has been registered but static type checker program couldn't be validated. \n")

        except subprocess.TimeoutExpired as exc:
            print(f"Process timed out.\n{exc}")
            print(
                f"DataApp {self.name} has been registered but static type checker program took more than 20 seconds to validate the code. \n")

        self._print_url(dataapp_svc, response)

    def _check_dataapp(self):
        """
        Check DataApp's source code.
        It checks source code by executing mypy program. 
        All errors and warnings will be saved in a log error file: errorLog_register.txt
        It shows a DataApp registration message displaying if an error has been found or not.
        """

        myoutput = open('errorLog_register.txt', 'w')
        output = subprocess.run(["mypy", f"{sys._getframe(1).f_code.co_filename}"], timeout=20, stdout=myoutput)

        if output.returncode != 0:
            print(
                f"DataApp {self.name} has been registered but may not work as expected. Please check errorLog_register.txt \n")
        else:
            print(f"DataApp {self.name} has been registered succesfully. \n")

    def _print_url(self, dataapp_svc, response: str):
        """
        Print a URL to the DataApp just been registered.
        """

        dict = json.loads(response.text)

        url = dataapp_svc.session.prefix_url

        address = f"{url}/app/data-apps/{self.name}/{dict['major']}/{dict['minor']}"
        address = address.strip()
        address = address.replace(' ', "%20")

        print("---------------------------------------------------------------------------------")
        print("DataApp Registered! \n")
        print(f"DataApp can be accessed by clicking here: {address} \n")

    def set_title(self, title: str):
        """
        Sets the DataApp's title.

        Parameters
        ----------
        title : str
            The title for the app.

        Examples
        --------
        >>> app.set_title('new title')             
        """
        self.title = title

    # def temporal_context(self,
    #                      name: str = None,
    #                      widgets: List[Widget] = None,
    #                      context_id: str = None):
    #     """
    #     Defines a temporal context for your dataApp.
    #
    #     Parameters
    #     ----------
    #     name : str, optional
    #         String with the temporal context name.
    #
    #     widgets : list[Widgets], optional
    #         List of Widgets inside the temporal context.
    #
    #     context_id : str, optional
    #         String with the temporal context ID.
    #
    #
    #     Returns
    #     -------
    #     New Temporal Context.
    #
    #     Examples
    #     --------
    #     >>> lc1 = app.line_chart(data)
    #     >>> lc2 = app.line_chart(data2)
    #     >>> tc = app.temporal_context('Range A',[lc,lc2])
    #     """
    #     widget_ids = []
    #     if widgets:
    #         for widget in widgets:
    #             if hasattr(widget, 'temporal_context'):
    #                 widget_ids.append(widget.widget_id)
    #             else:
    #                 raise Exception(f"Component {widget.widget_type} does not allow temporal context")
    #     temporal_context = TemporalContext(name, widget_ids, context_id)
    #     self.temporal_contexts.append(temporal_context)
    #     return temporal_context

    # def filtering_context(self,
    #                       name: str = None,
    #                       input_filter: List[MetadataField] = None,
    #                       context_id: str = None):
    #     """
    #     Defines a filtering context for your dataApp.
    #
    #     Parameters
    #     ----------
    #     name : str, optional
    #         String with the filtering context name.
    #
    #     input_filter : list, optional
    #         List of Widgets inside the temporal context.
    #
    #     context_id : str, optional
    #         String with the filtering context ID.
    #
    #     Returns
    #     -------
    #     New Filtering Context.
    #
    #     Examples
    #     --------
    #     TODO
    #     """
    #     input_filters_ids = []
    #     collection_id = None
    #     if input_filter:
    #         collection_ids = [mfield.collection.collection_id for mfield in input_filter]
    #         collection_ids_set = set(collection_ids)
    #         if len(set(collection_ids)) == 1:
    #             collection_id = collection_ids_set.pop()
    #             for widget in input_filter:
    #                 # if hasattr(widget, 'filtering_context'):
    #                 input_filters_ids.append(widget.widget_id)
    #                 # else:
    #                 #     raise Exception(f"Component {widget.widget_type} does not allow filtering context")
    #         else:
    #             raise Exception("Collection missmatch: All MetadataFields need to come from the same Collection.")
    #     filtering_context = FilteringContext(name, collection_id, input_filters_ids, context_id)
    #     self.filtering_contexts.append(filtering_context)
    #     return filtering_context

    def image(self,
              img: Optional[Union[str, bytes, Path, Figure]] = None,
              caption: Optional[str] = None,
              placeholder: Optional[Union[str, bytes, Path]] = None,
              **additional):
        """
        Adds a placeholder for a Image on a DataApp. You can load a local image file or generate one with Python.

        Parameters
        ----------
        img : str
            Path of Image to be included.

        caption : str, optional
            Caption for the image

        placeholder : str, optional
            Placeholder image

        Returns
        -------
        Image

        Examples
        --------
        >>> image = app.Image('path/to/image','Image 1')         

        .. rubric:: Bind compatibility

        You can bind this widget with this: 

        .. hlist::
            :columns: 1

            * str
            * bytes
            * :func:`~shapelets.apps.DataApp.path`
            * :func:`~shapelets.apps.DataApp.figure`
            * :func:`~shapelets.apps.DataApp.image`   

        .. rubric:: Bindable as

        You can bind this widget as: 

        *Currently this widget cannot be used as input in a binding function.*

        """
        return ImageWidget(img, caption, placeholder, parent_data_app=self, **additional)

    # def list(self,
    #          list_title: Optional[str] = None,
    #          items: Optional[List[Widget]] = [],
    #          **additional):
    #     """
    #     Adds a List of different elements to your dataApp.
    #     param items: List items.
    #     return ListWidget.
    #     """
    #     return ListWidget(list_title, items, parent_data_app=self, **additional)

    def number_input(self,
                     title: Optional[str] = None,
                     value: Optional[Union[int, float]] = None,
                     default_value: Optional[Union[int, float]] = None,
                     placeholder: Optional[str] = None,
                     min: Optional[Union[int, float]] = None,
                     max: Optional[Union[int, float]] = None,
                     step: Optional[Union[int, float]] = None,
                     text_style: Optional[dict] = None,
                     units: Optional[str] = None,
                     **additional) -> NumberInputWidget:
        """
        A basic widget for getting the user input as a number field.

        Parameters
        ----------
        title : str, optional
            String with the widget title. It will be placed on top of the widget box.

        value : int or float, optional
            Define number value.

        default_value : int or float, optional
            Default value for the widget.

        placeholder : str, optional
            Text showed inside the widget by default.

        min : int or float, optional
            Minimum value of the widget.

        max : int or float, optional
            Maximum value of the widget.

        step : int or float, optional
            The granularity the widget can step through values. Must greater than 0, and be divided by (max - min).

        text_style : dict, optional
            Dict to customize text: font size, font type y font style.

        units : str, optional
            Specifies the format of the value presented, for example %, KWh, Kmh, etc.


        Returns
        -------
        Number Input.

        Examples
        --------
        >>> number_input = app.number_input()

        >>> number_input = app.number_input(min=1,max=100,step=5,units='%')


        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * int
            * float
            * :func:`~shapelets.apps.DataApp.number_input`

        .. rubric:: Bindable as

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * int
            * float

        """

        return NumberInputWidget(title, value, default_value, placeholder, min, max, step, text_style, units,
                                 parent_data_app=self, **additional)

    # def sequence_list(self,
    #                   title: Union[str, Node] = None,
    #                   collection: Union[Collection, Node] = None,
    #                   temporal_context: TemporalContext = None,
    #                   filtering_context: FilteringContext = None,
    #                   **additional):
    #     return SequenceList(
    #         title,
    #         collection,
    #         temporal_context,
    #         filtering_context,
    #         **additional)

    def text_input(self,
                   title: Optional[str] = None,
                   value: Optional[Union[str, int, float]] = None,
                   placeholder: Optional[str] = None,
                   multiline: Optional[bool] = None,
                   text_style: Optional[dict] = None,
                   toolbar: Optional[bool] = None,
                   markdown: Optional[bool] = None,
                   width: Optional[Union[int, float]] = None,
                   **additional):
        """
        A basic widget for getting the user input as a text field.

        Parameters
        ----------
        title : str, optional
            String with the widget title. It will be placed on top of the widget box.

        value : str, int or float, optional
            Default value.

        placeholder : str, optional
            Text showed inside the widget by default.

        multiline : bool, optional
            Show text in multiline.

        text_style : dict, optional
            Dict to customize text: font size, font type y font style.

        toolbar : bool, optional
            Show toolbar on top of the widget.

        width : int or float, optional
            width of the text input. It represents a percentage value.

        markdown : bool, optional
            Flag to indicate if markdown format in in input text.

        Returns
        -------
        Text Input.

        Examples
        --------
        >>> text_input = app.text_input() 

        >>> text_input = app.text_input(title="Find object",placeholder="Write here", markdown=True)

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * int
            * :func:`~shapelets.apps.DataApp.text_input`


        .. rubric:: Bindable as

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * str
            * int
        """
        return TextInputWidget(title=title, value=value, placeholder=placeholder, multiline=multiline,
                               text_style=text_style, toolbar=toolbar, markdown=markdown, width=width,
                               parent_data_app=self, **additional)

    def datetime_selector(self,
                          title: str = None,
                          date_time: Union[float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                          min_date: Union[float, int, str, datetime.date] = None,
                          max_date: Union[float, int, str, datetime.date] = None,
                          **additional) -> DateSelectorWidget:
        """
        Creates a box that allows the user input as date.

        Parameters
        ----------
        title : str, optional
            String with the widget title. It will be placed on top of the widget box.

        date_time : float, int, str, datetime.datetime, datetime.date or datetime.time, optional
            Preloaded date.

        min_date : float, int, str or datetime.datetime, optional
            Minimum date allowed.

        max_date : float, int, str or datetime.datetime, optional
            Maximum date allowed.


        Returns
        -------
        DateSelectorWidget

        Examples
        --------
        >>> date_selector = app.datetime_selector()

        >>> # Datetime selector with int
        >>> dt = app.datetime_selector(date_time=1667468964,
        >>>                             min_date=1667460964,
        >>>                             max_date=1676913679)

        >>> # Datetime selector with datetime
        >>> dt = app.datetime_selector(date_time=datetime(year=2022, month=1, day=1, hour=18, minute=20))

        >>> # Datetime selector with date
        >>> dt = app.datetime_selector(date_time=date(year=2022, month=1, day=1),
        >>>                             min_date=date(year=1950, month=1, day=1),
        >>>                             max_date=date(year=2050, month=1, day=1))

        >>> # Datetime selector with strings
        >>> dt = app.datetime_selector(date_time='1970-01-01',
        >>>                             min_date='1955-01-01',
        >>>                             max_date='2100-01-01')



        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * int
            * :func:`~shapelets.apps.DataApp.datetime_selector`
            * datetime.datetime
            * datetime.date

        .. rubric:: Bindable as

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * str
        """
        return DateSelectorWidget(title, date_time, min_date, max_date, parent_data_app=self, **additional)

    def datetime_range_selector(self,
                                title: str = None,
                                start_datetime: Union[
                                    float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                                end_datetime: Union[
                                    float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                                min_datetime: Union[
                                    float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                                max_datetime: Union[
                                    float, int, str, datetime.datetime, datetime.date, datetime.time] = None,
                                **additional) -> DatetimeRangeSelectorWidget:
        """
        Creates a box that allows the user input as date range.

        Parameters
        ----------
        title : str, optional
            String with the widget title. It will be placed on top of the widget box.

        start_datetime : float, int, str, datetime.datetime, datetime.date or datetime.time, optional
            Preloaded start range date.

        end_datetime : float, int, str, datetime.datetime, datetime.date or datetime.time, optional
            Preloaded end range date.

        min_datetime : float, int, str, datetime.datetime, datetime.date or datetime.time, optional
            Minimum date allowed.

        max_datetime : float, int, str, datetime.datetime, datetime.date or datetime.time, optional
            Maximum date allowed.

        Returns
        -------
        DatetimeRangeSelectorWidget

        Examples
        --------
        >>> date_selector = app.datetime_range_selector()

        >>> # Datetime range selector with int
        >>> dt = app.datetime_range_selector(start_datetime=1667468964,
        >>>                                 end_datetime=1667468964,
        >>>                                 min_datetime=1667468964,
        >>>                                 max_datetime=1667468964)

        >>> # Datetime range selector with date
        >>> dt = app.datetime_range_selector(start_datetime=date(year=2022, month=11, day=1),
        >>>                                 end_datetime=date(year=2022, month=11, day=10),
        >>>                                 min_datetime=date(year=1950, month=1, day=1),
        >>>                                 max_datetime=date(year=2050, month=1, day=1))

        >>> # Datetime range selector with datetime
        >>> dt = app.datetime_range_selector(start_datetime=datetime(year=2022, month=11, day=1, hour=21),
        >>>                                 end_datetime=datetime(year=2022, month=11, day=10, hour=19, second=5),
        >>>                                 min_datetime=date(year=1950, month=1, day=1),
        >>>                                 max_datetime=date(year=2050, month=1, day=1))

        >>> # Datetime range selector with string
        >>> dt = app.datetime_range_selector(start_datetime='2022-01-01 00:05:00',
        >>>                                 end_datetime='2022-12-31 23:59:59',
        >>>                                 min_datetime='1955-01-01',
        >>>                                 max_datetime='2100-01-01')



        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * :func:`~shapelets.apps.DataApp.datetime_range_selector`

        .. rubric:: Bindable as

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * tuple
        """
        return DatetimeRangeSelectorWidget(title, start_datetime, end_datetime, min_datetime, max_datetime,
                                           parent_data_app=self,
                                           **additional)

    def slider(self,
               title: str = None,
               value: Union[str, int, float, List[int], List[float], List[str]] = None,
               min_value: Union[int, float] = None,
               max_value: Union[int, float] = None,
               step: Union[int, float] = None,
               range: Optional[bool] = None,
               options: Union[List, dict] = None,
               **additional) -> SliderWidget:
        """
        Creates a slider that lets a user pick a value from a set range by moving a knob.

        Parameters
        ----------
        title : str, optional
            String with the Slider title. It will be placed on top of the Slider.

        value : str, int, float, List[int], List[float], List[str], optional
            Initial value of the slider

        min_value : int or float, optional
            Minimum value of the slider.

        max_value : int or float, optional
            Maximum value of the slider.

        step : int or float, optional
            The granularity the slider can step through values. Must greater than 0, and be divided by (max - min)

        range : bool, optional
            Dual thumb mode.

        options : list or dict, optional
            Tick mark of the slider. It can be defined as list of lists ([[0,1],["Cold","Warm"]]) or as a dictionary ({0: "Cold", 1: "Warm"})


        Returns
        -------
        SliderWidget

        Examples
        --------
        >>> slider = app.slider()

        >>> slider = app.slider(title="Slider with default value to 5", min_value=0, max_value=10, step=1, value=5)


        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * int
            * float
            * list
            * :func:`~shapelets.apps.DataApp.slider`


        .. rubric:: Bindable as

        You can bind this widget as: 

        If you are using `range=False`

        .. hlist::
            :columns: 1

            * int
            * float

        If you are using `range=True`

        .. hlist::
            :columns: 1

            * tuple 
        """

        return SliderWidget(title, value, min_value, max_value, step, range, options, parent_data_app=self,
                            **additional)

    def button(self, text: str = "", **additional) -> Button:
        """
        Creates a button.

        Parameters
        ----------
        text : str, optional
            String placed inside the button.

        Returns
        -------
        Button

        Examples
        --------
        >>> button = app.button("Press me") 

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * :func:`~shapelets.apps.DataApp.button`

        Note: bind function will change button text.

        """
        return Button(text, parent_data_app=self, **additional)

    def timer(self,
              title: str = None,
              every: Union[int, float] = None,
              start_delay: int = None,
              times: int = None,
              hidden: bool = False,
              start_on_init: bool = False,
              **additional) -> TimerWidget:
        """
        Creates a Timer for your dataApp.

        Parameters
        ----------
        title : str, optional
            String with the Timer title. It will be placed on top of the Timer.

        every : int or float, optional
            Defines how often the Timer is executed in seconds.

        start_delay : int, optional
            Defines a start delay for the Timer.

        times : int, optional
            Defines the amount of cycles the Timer is repeated.

        hidden : bool, optional
            Should the timer be hidden?

        start_on_init : bool, optional
            Should the timer start on init

        Returns
        -------
        Timer

        Examples
        --------
        >>> timer = app.timer(title="Timer", every=1.0, times=10)         


        """
        return TimerWidget(title, every, start_delay, times, hidden, start_on_init, parent_data_app=self, **additional)

    def altair_chart(self, title: Optional[str] = None, chart: Optional[any] = None, **additional) -> AltairChartWidget:
        """
        Creates an Vega-Altair chart: a declarative statistical visualization library for Python
        (https://altair-viz.github.io/index.html).

        Parameters
        ----------
        title : str, optional
            String with the Altair Chart title. It will be placed on top of the Chart.

        chart : any , optional
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
        return AltairChartWidget(title, chart, parent_data_app=self, **additional)

    def folium_chart(self, title: Optional[str] = None, folium: Optional[any] = None,
                     **additional) -> FoliumChartWidget:
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
        return FoliumChartWidget(title, folium, parent_data_app=self, **additional)

    # def plotly_chart(self, title: Optional[str] = None, fig: Optional[any] = None, **additional) -> PlotlyChartWidget:
    #     """
    #     Creates a Plotly graph. Plotly's Python graphing library makes interactive, publication-quality graphs
    #     (https://plotly.com/graphing-libraries).
    #     param fig: Loads a plotly figure which includes a JSON specification for Plotly Chart.
    #     return PlotlyChartWidget
    #     """
    #     return PlotlyChartWidget(title=title, value=fig, **additional)

    def vertical_layout(self,
                        title: str = None,
                        panel_id: str = None,
                        vertical_align: Optional[Literal["start", "center", "end"]] = "start",
                        span: int = None,
                        offset: int = None,
                        **additional) -> VerticalLayoutWidget:
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

        span: int, optional
            Columns for this vertical layout, The column grid system is a value of 1-24 to represent its range spans.

        offset: int, optional
            Offset can set the column to the right side. Values of 1-24 

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
        return VerticalLayoutWidget(panel_title=title, panel_id=panel_id, vertical_align=vertical_align, span=span,
                                    offset=offset,
                                    parent_data_app=self, **additional)

    def horizontal_layout(self,
                          title: str = None,
                          panel_id: str = None,
                          horizontal_align: Optional[Literal["start", "center", "end"]] = "start",
                          vertical_align: Optional[Literal["start", "center", "end"]] = "start",
                          **additional) -> HorizontalLayoutWidget:
        """
        Defines a layout where widgets are arranged side by side horizontally.

        Parameters
        ----------
        title : str, optional
            String with the Panel title. It will be placed on top of the Panel.

        panel_id : str, optional
            Panel ID.

        horizontal_align : str, optional
            Select how widgets are align horizontally: start, center, end. Default: start.

        vertical_align : str, optional
            Select how widgets are align vertically: start, center, end. Default: start.

        Returns
        -------
        HorizontalLayout.

        Examples
        --------
        >>> hl = app.horizontal_layout()
        >>> # Create buttons and place multiple text inputs in the horizontal layout
        >>> txt1 = app.text_input("Text input #1")
        >>> hl.place(txt1)

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * :func:`~shapelets.apps.DataApp.horizontal_layout`

        .. rubric:: Bindable as

        You can bind this widget as: 

        *Currently this widget cannot be used as input in a binding function.*             
        """
        return HorizontalLayoutWidget(panel_title=title,
                                      panel_id=panel_id,
                                      horizontal_align=horizontal_align,
                                      vertical_align=vertical_align,
                                      parent_data_app=self,
                                      **additional)

    # def grid_panel(self,
    #                num_rows: int,
    #                num_cols: int,
    #                title: str = None,
    #                panel_id: str = None,
    #                **additional):
    #     """
    #     Defines a Grid Panel.
    #     param num_rows: Number of rows.
    #     param num_cols: Number of columns.
    #     param title: String with the Panel title. It will be placed on top of the Panel.
    #     param panel_id: Panel ID.
    #     return GridPanel.
    #     """
    #     return GridPanel(num_rows, num_cols, panel_title=title, panel_id=panel_id, **additional)

    def tabs_layout(self, title: str = None, **additional) -> TabsLayoutWidget:
        """
        Defines a Tabs Layout, a layout that provides a horizontal layout to display tabs.

        Parameters
        ----------
        title : str, optional
            String with the Panel title. It will be placed on top of the Panel.

        Returns
        -------
        TabsLayout.

        Examples
        --------
        >>> # Create two vertical layouts
        >>> vf = app.vertical_layout()
        >>> vf2 = app.vertical_layout()
        >>> # Create a tabs layout
        >>> tabs_fp = app.tabs_layout("My tabs layout")
        >>> # Create two tabs and add a vertical layout in each of them 
        >>> tabs_fp.add_tab("Tab 1", vf)
        >>> tabs_fp.add_tab("Tab 2", vf2)

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * :func:`~shapelets.apps.DataApp.tabs_layout`

        .. rubric:: Bindable as

        You can bind this widget as: 

        *Currently this widget cannot be used as input in a binding function.*              
        """
        return TabsLayoutWidget(title, parent_data_app=self, **additional)

    def line_chart(self,
                   data: Optional[LineChartValueType] = None,
                   title: str = None,
                   views: List[View] = [],
                   # temporal_context: TemporalContext = None,
                   # filtering_context: FilteringContext = None,
                   multi_line_chart: bool = True,
                   multi_lane: Optional[bool] = True,
                   **additional) -> LineChartWidget:
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
        return LineChartWidget(
            data,
            title,
            views,
            # temporal_context,
            # filtering_context,
            multi_line_chart,
            multi_lane,
            parent_data_app=self,
            **additional)

    # def metadata_field(self,
    #                    field_name: str,
    #                    field_type: MetadataType,
    #                    collection: Collection,
    #                    name: str = None,
    #                    **additional):
    #     """
    #     Creates a Metadata Field
    #     param field_name: Metadata Name.
    #     param field_type: Metadata Field.
    #     param collection: Collection where the Metadata Field belongs.
    #     param name: Internal Name of the Metadata Field object.
    #     return MetadataField.
    #     """
    #     return MetadataField(field_name, field_type, collection, name, parent_data_app=self, **additional)

    # def collection_selector(self,
    #                         default_collection: Collection = None,
    #                         default_sequence: Sequence = None,
    #                         name: str = None,
    #                         title: str = None,
    #                         collection_label: str = None,
    #                         sequence_label: str = None,
    #                         **additional):
    #     """
    #     Creates a Collection Selector, a pair of drop-down menus that allows the selection of any particular sequence
    #     from any given collection that the user has registered.
    #     param default_collection: Default Collection selected in the Collection Selector.
    #     param default_sequence: Default Sequence selected in the Collection Selector.
    #     param name: Internal name of the Collection Selector object.
    #     param title: String with the Collection Selector title. It will be placed on top of the Collection Selector.
    #     param collection_label: String with the label for the Collection drop-down menu.
    #     param sequence_label: String with the label for the Sequence drop-down menu.
    #     return CollectionSelector.
    #     """
    #     return CollectionSelector(default_collection,
    #                               default_sequence,
    #                               name,
    #                               title,
    #                               collection_label,
    #                               sequence_label,
    #                               parent_data_app=self,
    #                               **additional)

    # def sequence_selector(self,
    #                       collection: Collection = None,
    #                       sequences: List[Sequence] = None,
    #                       default_sequence: Sequence = None,
    #                       name: str = None,
    #                       title: str = None,
    #                       **additional):
    #     """
    #     Creates a Sequence Selector, a drop down menu that allow the selection of any particular sequence.
    #     param collection: Collection containing the Sequences to be represented in the Sequence Selector.
    #     param sequences: List of Sequences to be represented in the Sequence Selector.
    #     param default_sequence: Default Sequence selected in the Sequence Selector.
    #     param name: Internal name of the Sequence Selector object.
    #     param title: String with the Sequence Selector title. It will be placed on top of the Sequence Selector.
    #     return SequenceSelector.
    #     """
    #     return SequenceSelector(collection,
    #                             sequences,
    #                             default_sequence,
    #                             name,
    #                             title,
    #                             parent_data_app=self,
    #                             **additional)

    # def multi_sequence_selector(self,
    #                             collection: Collection = None,
    #                             sequences: List[Sequence] = None,
    #                             default_sequence: List[Sequence] = None,
    #                             name: str = None,
    #                             title: str = None,
    #                             **additional):
    #     """
    #     Creates a Multi Sequence Selector, a drop down menu that allow the selection of multiple sequences.
    #     param collection: Collection containing the Sequences to be represented in the Sequence Selector.
    #     param sequences: List of Sequences to be represented in the Sequence Selector.
    #     param default_sequence: Default Sequence selected in the Sequence Selector.
    #     param name: Internal name of the Sequence Selector object.
    #     param title: String with the Sequence Selector title. It will be placed on top of the Sequence Selector.
    #     return MultiSequenceSelector.
    #     """
    #     return MultiSequenceSelector(collection,
    #                                  sequences,
    #                                  default_sequence,
    #                                  name,
    #                                  title,
    #                                  parent_data_app=self,
    #                                  **additional)

    def selector(self,
                 options: Optional[List[Union[int, float, str]]] = None,
                 title: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 default: Optional[Union[str, int, float]] = None,
                 allow_multi_selection: Optional[bool] = None,
                 width: Optional[Union[int, float]] = None,
                 **additional) -> SelectorWidget:
        """
        Creates a dropdown menu for displaying multiple choices.

        Parameters
        ----------
        options : int, float, str or any, optional
            A list of items to be chosen.

        title : str,  optional
            String with the Selector title. It will be placed on top of the Selector.

        placeholder : str,  optional
            Text showed inside the Selector by default.

        default : str, int, float or list,  optional
            Default value.

        allow_multi_selection : bool, optional
            Allows selecting multiple values.

        width : int or float, optional
            width of the selector. It represents a percentage value.

        Returns
        -------
        Selector

        Examples
        --------
        >>> selector = app.selector(title="My Selector", options=['a','b','c']) 


        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * int
            * float
            * list
            * :func:`~shapelets.apps.DataApp.selector`

        .. rubric:: Bindable as 

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * tuple
        """
        return SelectorWidget(options=options, title=title, placeholder=placeholder, default=default,
                              allow_multi_selection=allow_multi_selection, width=width, parent_data_app=self,
                              **additional)

    def radio_group(self,
                    options: Optional[List[Union[int, float, str]]] = None,
                    title: Optional[str] = None,
                    label_by: Optional[str] = None,
                    value_by: Optional[str] = None,
                    value: Optional[List[Union[int, float, str, any]]] = None,
                    style: Literal["radio", "button"] = None,
                    **additional: object) -> RadioGroupWidget:
        """
        Creates a radio button group for displaying multiple choices and allows to select one value out of a set.

        Parameters
        ----------
        options :list, optional
            A list of items to be chosen.

        title : str, optional
            String with the RadioGroup title. It will be placed on top of the RadioGroup.

        label_by : str, optional
            Selects key to use as label.

        value_by : str, optional
            Selects key to use as value.

        value : int, float or str, optional
            Default value.

        style : "radio" or "button" , optional
            Radio Group style.

        Returns
        -------
        RadioGroup

        Examples
        --------
        >>> radiogroup1 = app.radio_group([1, 2, 3], value=2)

        >>> # Radio group with dict values, index_by, label_by and value_by property
        >>> radiogroup2 = app.radio_group(
        >>>     [{"id": 1, "label": "world", "value": "bar"}, 
        >>>     {"id": 2, "label": "moon", "value": "baz"}],
        >>>     label_by="label",
        >>>     value_by="value")


        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * int
            * float
            * list
            * :func:`~shapelets.apps.DataApp.radio_group`

        .. rubric:: Bindable as 

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * str
            * int
            * float

        """
        return RadioGroupWidget(options, title, label_by, value_by, value, style,
                                parent_data_app=self, **additional)

    # def bar_chart(self,
    #               data: Union[List[int], List[float], NDArray, Node],
    #               categories: Union[List[str], List[int], List[float], NDArray, Node] = None,
    #               name: Union[str, Node] = None,
    #               title: Union[str, Node] = None,
    #               **additional):
    #     """
    #     Produces a Bar Chart figure for your dataApp.
    #     param data: Data to be included in the Bar Chart.
    #     param categories: Categories to be included in the Bar Chart.
    #     param name: Internal name of the Bar Chart object.
    #     param title: String with the Bar Chart title. It will be placed on top of the Bar Chart.
    #     return BarChart
    #     """
    #     return BarChart(data, categories, name, title, **additional)

    # def heatmap(self,
    #             x_axis: Union[List[int], List[float], List[str], NDArray, Node],
    #             y_axis: Union[List[int], List[float], List[str], NDArray, Node],
    #             z_axis: Union[List[int], List[float], NDArray, Node],
    #             name: Union[str, Node] = None,
    #             title: Union[str, Node] = None):
    #     """
    #     Produces a Heatmap figure for your dataApp.
    #     param x_axis: X axis to be included in the heatmap.
    #     param y_axis: Y Axis to be included in the heatmap.
    #     param z_axis: Z axis to be included in the heatmap. Is represented with color.
    #     param name: Internal name of the Heatmap object.
    #     param title: String with the Heatmap title. It will be placed on top of the Heatmap.
    #     return HeatMap
    #     """
    #     return HeatMap(x_axis, y_axis, z_axis, name, title)

    # def histogram(self,
    #               x: Union[List[int], List[float], NDArray, Node],
    #               bins: Union[int, float, Node] = None,
    #               cumulative: Union[bool, Node] = False,
    #               **additional):
    #     """
    #     Produces a Histogram figure for your dataApp.
    #     param x: Data to be included in the Histogram.
    #     param bins: Amount of bins for the Histogram.
    #     param cumulative: Should values be cumulative?
    #     return Histogram
    #     """
    #     return Histogram(x, bins, cumulative, **additional)

    # @overload
    # def scatter_plot(self,
    #                  x_axis: Union[List[int], List[float], NDArray, Node],
    #                  y_axis: Union[List[int], List[float], NDArray, Node] = None,
    #                  size: Union[List[int], List[float], NDArray, Node] = None,
    #                  color: Union[List[int], List[float], NDArray, Node] = None,
    #                  title: Union[str, Node] = None,
    #                  trend_line: bool = False):
    #     ...
    #
    # @overload
    # def scatter_plot(self,
    #                  x_axis: Union[List[int], List[float], NDArray, Node],
    #                  y_axis: Union[List[int], List[float], NDArray, Node] = None,
    #                  size: Union[List[int], List[float], NDArray, Node] = None,
    #                  categories: Union[List[int], List[float], List[str], NDArray, Node] = None,
    #                  title: Union[str, Node] = None,
    #                  trend_line: bool = False):
    #     ...
    #
    # def scatter_plot(self,
    #                  x_axis: Union[List[int], List[float], NDArray, Node],
    #                  y_axis: Union[List[int], List[float], NDArray, Node],
    #                  size: Union[List[int], List[float], NDArray, Node] = None,
    #                  color: Union[List[int], List[float], NDArray, Node] = None,
    #                  categories: Union[List[int], List[float], List[str], NDArray, Node] = None,
    #                  name: str = None,
    #                  title: Union[str, Node] = None,
    #                  trend_line: bool = False,
    #                  **additional):
    #     """
    #     Produces a Scatter Plot figure for your dataApp.
    #     param x_axis: X axis values.
    #     param y_axis: Y axis values.
    #     param size: Add size of each point.
    #     param color: Add color scale for each point.
    #     param categories: Category of each point.
    #     param name: Internal name of the Scatter Plot object.
    #     param title: String with the Scatter Plot title. It will be placed on top of the Scatter Plot.
    #     param trend_line: Add a trend line to the Scatter Plot.
    #     return ScatterPlot
    #     """
    #     return ScatterPlot(x_axis, y_axis, size, color, categories, name, title, trend_line, **additional)
    #
    # def pie_chart(self,
    #               data: Union[List[int], List[float], NDArray, Node],
    #               categories: Union[List[int], List[float], List[str], NDArray, Node] = None,
    #               name: str = None,
    #               title: Union[str, Node] = None,
    #               **additional):
    #     """
    #     Produces a Pie Chart figure for your dataApp.
    #     param data: Data to be included in the Pie Chart.
    #     param categories: Categories to be included in the Pie Chart.
    #     param name: Internal name of the Pie Chart object.
    #     param title: String with the Pie Chart title. It will be placed on top of the Pie Chart.
    #     return PieChart
    #     """
    #     return PieChart(data, categories, name, title, **additional)
    #
    # def donut_chart(self,
    #                 data: Union[List[int], List[float], NDArray, Node],
    #                 categories: Union[List[int], List[float], List[str], NDArray, Node] = None,
    #                 name: str = None,
    #                 title: Union[str, Node] = None,
    #                 **additional):
    #     """
    #     Produces a Donut Chart figure for your dataApp.
    #     param data: Data to be included in the Donut Chart.
    #     param categories: Categories to be included in the Donut Chart.
    #     param name: Internal name of the Donut Chart object.
    #     param title: String with the Donut Chart title. It will be placed on top of the Donut Chart.
    #     return DonutChart
    #     """
    #     return DonutChart(data, categories, name, title, **additional)
    #
    # def polar_area_chart(self,
    #                      categories: Union[List[int], List[float], List[str], NDArray, Node],
    #                      data: Union[List[int], List[float], NDArray, Node],
    #                      name: str = None,
    #                      title: Union[str, Node] = None,
    #                      **additional):
    #     """
    #     Produces a Polar Area Chart figure for your dataApp.
    #     param data: Data to be included in the Polar Area Chart.
    #     param categories: Categories to be included in the Polar Area Chart.
    #     param name: Internal name of the Polar Area Chart object.
    #     param title: String with the Polar Area Chart title. It will be placed on top of the Polar Area Chart.
    #     return PieChart
    #     """
    #     return PolarArea(categories, data, name, title, **additional)
    #
    # def radar_area_chart(self,
    #                      categories: Union[List[int], List[float], List[str]],
    #                      data: Union[List[int], List[float]],
    #                      groups: Union[List[int], List[float], List[str]],
    #                      name: str = None,
    #                      title: str = None,
    #                      **additional):
    #     """
    #     Produces a Radar Area Chart figure for your dataApp
    #     param categories: Categories to be included in the Radar Area Chart.
    #     param data: Data to be included in the Radar Area Chart.
    #     param groups: Defines the grouping of the data for the Radar Area Chart.
    #     param name: Internal name of the Radar Area Chart object.
    #     param title: String with the Radar Area Chart title. It will be placed on top of the Radar Area Chart.
    #     return RadarArea.
    #     """
    #     return RadarAreaWidget(categories, data, groups, name, title, **additional)

    def checkbox(self,
                 title: Optional[str] = None,
                 checked: Optional[bool] = False,
                 toggle: Optional[bool] = None,
                 **additional) -> CheckboxWidget:
        """
        Creates a Checkbox.

        Parameters
        ----------
        title : str, optional
            Text associated to the checkbox.

        checked : bool, optional
            Param to indicate the status of the widget

        toggle : bool, optional
            Param to display the widget as a toggle button

        Returns
        -------
        Checkbox.

        Examples
        --------
        >>> control = app.checkbox(title='Option', toggle=True)

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * bool
            * :func:`~shapelets.apps.DataApp.checkbox`

        .. rubric:: Bindable as 

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * bool

        """
        return CheckboxWidget(title=title, checked=checked, toggle=toggle, parent_data_app=self, **additional)

    def text(self,
             value: Optional[Union[str, int, float]] = None,
             title: Optional[str] = None,
             text_style: Optional[dict] = None,
             markdown: Optional[bool] = None,
             **additional) -> TextWidget:
        """
        Creates a Label.

        Parameters
        ----------
        value : str, int or float, optional
            Text value of the widget.

        title : str, optional
            Title of the widget.

        text_style : dict, optional
            Text style for the label

        markdown : bool, optional
            Flag to indicate if Label is markdown


        Returns
        -------
        Label

        Examples
        --------
        >>> text1 = app.text("Hello world!")

        >>> text1 = app.text("# Hello world!", markdown = True)


        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * int
            * float
            * :func:`~shapelets.apps.DataApp.text`
            * datetime

        .. rubric:: Bindable as 

        You can bind this widget as: 

        .. hlist::
            :columns: 1

            * str
            * int
            * float
            * :func:`~shapelets.apps.DataApp.text`        

        """
        return TextWidget(value=value, title=title, text_style=text_style, markdown=markdown,
                          parent_data_app=self, **additional)

    def progress(self,
                 value: Optional[Union[str, int, float]] = None,
                 title: Optional[str] = None,
                 type: Optional[Literal["line", "circle", "dashboard"]] = None,
                 size: Optional[Union[int, Literal["small", "regular"]]] = None,
                 status: Optional[Literal["success", "exception", "normal", "active"]] = None,
                 stroke_color: Optional[Union[str, List[str], Literal["shapelets"]]] = None,
                 stroke_width: Optional[int] = None,
                 show_info: Optional[bool] = None,
                 **additional):
        """
        TODO
        """
        return ProgressWidget(value=value, title=title, type=type, size=size, status=status,
                              stroke_color=stroke_color, stroke_width=stroke_width, show_info=show_info,
                              parent_data_app=self, **additional)

    def table(self,
              data: Union[pd.DataFrame, DataSet] = None,
              rows_per_page: Optional[int] = None,
              tools_visible: Optional[bool] = None,
              conditional_formats: Optional[List[Union[Condition, dict]]] = None,
              date_format: Optional[str] = None,
              **additional):
        """
        Displays rows of data.

        Parameters
        ----------
        data : Dataset or pd.Dataframe, optional
            Data to be included in the Table.

        rows_per_page : int, optional
            number of rows per page to show

        tools_visible : int, optional
            show/hide header, header bold and rowcolumn controls

        conditional_formats: List[Dict, Conditional], optional
            Add format to a value applying any condition. There are two types of conditional format:
                * Range: Allow to modify the color and background color of a numeric value
                * Case: Allow to modify the color and brackgorund color of a string value
            For example:
                >>> myformat = {
                >>>     "column": "T1",
                >>>     "type": "range",
                >>>     "conditions": [
                >>>         { "min": 0, "max": 20, "backcolor": "#ff0000", "color": "#ffffff" },
                >>>         { "min": 20,"max": 40, "backcolor": "#ff860a" },
                >>>         { "min": 40,"max": 42, "color": "#ff860a" },
                >>>         { "min": 44,"max": 100, "backcolor": "#00aa00" }
                >>>     ]
                >>> },
                >>> {
                >>>     "column": "Estado",
                >>>     "type": "case",
                >>>     "conditions": [
                >>>         { "value": "Peligro", "backcolor": "#ff0000", "color": "#ffffff" },
                >>>         { "value": "Precaución", "backcolor": "#000077", "color": "#ffffff" },
                >>>         { "value": "OK", "backcolor": "#00aa00", "color": "#ffffff" }
                >>>     ]
                >>> }
                >>> table = app.table(data=data,conditional_format=my_format)

        date_format: str, Optional
            If a column has a type timestamp, a format could be provided to trasnform the date.

        Returns
        -------
        Table

        Examples
        --------
        >>> table1 = app.table(df) 


        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * Shapelets Dataset
            * Pandas DataFrame
            * list
            * :func:`~shapelets.apps.DataApp.table`

        .. rubric:: Bindable as 

        You can bind this widget as: 

        *Currently this widget cannot be used as input in a binding function.*  

        """
        return TableWidget(data=data, rows_per_page=rows_per_page, tools_visible=tools_visible,
                           conditional_formats=conditional_formats, parent_data_app=self, date_format=date_format,
                           **additional)

    def gauge(self,
              title: Optional[str] = None,
              value: Optional[Union[int, float]] = None,
              **additional) -> GaugeWidget:
        """
        Creates a Gauge.

        Parameters
        ----------
        title : str, optional
            Text associated to the Gauge.

        value : int, float, optional
            Param to indicate the value of the widget. Must be between [0,1], cause 1 equals 100%. 

        Returns
        -------
        Gauge.

        Examples
        --------
        >>> gauge = app.gauge(title='Title', value=0.25)

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * int
            * float
            * :func:`~shapelets.apps.DataApp.gauge`

        .. rubric:: Bindable as

        You can bind this widget as:

        .. hlist::
            :columns: 1

            * int
            * float
            * string

        """
        return GaugeWidget(title=title, value=value,
                           parent_data_app=self, **additional)

    def metric(self,
               title: Optional[str] = None,
               value: Optional[str] = None,
               unit: Optional[str] = None,
               delta: Optional[str] = None,
               align: Optional[Literal["right", "left"]] = None,
               **additional) -> MetricWidget:
        """
        Creates a Metric.

        Parameters
        ----------
        title : str, optional
            Text associated to the metric widget.

        value : str, optional
            Param to indicate the value of the widget

        unit : str, optional
            Unit of the widget

        delta : str, optional
            Delta of the metric

        align : str, optional
            Select how the metric is aligned vertically: right or left.

        Returns
        -------
        Metric.

        Examples
        --------
        >>> metric = app.metric(title='Title', value="2023,46", unit="$", delta="+20,25", align="right")

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * str
            * int
            * float
            * :func:`~shapelets.apps.DataApp.metric`

        .. rubric:: Bindable as

        You can bind this widget as:

        .. hlist::
            :columns: 1

            * str
            * int
            * float

            """
        return MetricWidget(title=title, value=value, unit=unit, delta=delta, align=align,
                            parent_data_app=self, **additional)

    def ring(self,
             title: Optional[str] = None,
             value: Optional[Union[int, float]] = None,
             color: Optional[str] = None,
             **additional) -> RingWidget:
        """
        Creates a Ring.

        Parameters
        ----------
        title : str, optional
            Text associated to the Ring.

        value : int, float, optional
            Param to indicate the value of the widget as a percentage

        color : str, optional
            Color to display the widget

        Returns
        -------
        Ring.

        Examples
        --------
        >>> ring = app.ring(title='Title', value=25, color="Red")

        .. rubric:: Bind compatibility

        You can bind this widget with this:

        .. hlist::
            :columns: 1

            * int
            * float
            * :func:`~shapelets.apps.DataApp.ring`

        .. rubric:: Bindable as

        You can bind this widget as:

        .. hlist::
            :columns: 1

            * int
            * float
            * string

            """

        return RingWidget(title=title, value=value, color=color,
                          parent_data_app=self, **additional)

    def place(self, widget: Widget, *args, **kwargs):
        """
        Places a widget into the dataApp.

        Parameters
        ----------
        widget : Widget
            Widget to be included in the dataApp.

        Examples
        --------
        >>> app.place(my_widget)

        >>> layout.place(my_widget)

        """
        self.main_panel.place(widget, *args, **kwargs)

    def to_dict_widget(self):
        self_dict = {
            AttributeNames.ID.value: self.name,
            AttributeNames.NAME.value: self.name,
            AttributeNames.DESCRIPTION.value: self.description,
            AttributeNames.VERSION.value: self.version,
            AttributeNames.TAGS.value: self.tags,
            AttributeNames.TEMPORAL_CONTEXTS.value: self.temporal_contexts,
            AttributeNames.FILTERING_CONTEXTS.value: self.filtering_contexts
        }
        if self.functions and self.functions is not None:
            # Remove serialized body so it's not shown in the spec.
            for key, item in self.functions.items():
                item.pop("ser_body", None)
            self_dict.update({
                AttributeNames.FUNCTIONS.value: self.functions
            })
        else:
            self_dict.update({
                AttributeNames.FUNCTIONS.value: []
            })

        if hasattr(self, AttributeNames.TITLE.value):
            self_dict.update({
                AttributeNames.TITLE.value: self.title
            })
        self_dict[AttributeNames.MAIN_PANEL.value] = self.main_panel.to_dict_widget()
        temporal_context = []
        for temporal in self.temporal_contexts:
            temporal_context.append(temporal.to_dict())
        self_dict[AttributeNames.TEMPORAL_CONTEXTS.value] = temporal_context

        filtering_context = []
        for filter_context in self.filtering_contexts:
            filtering_context.append(filter_context.to_dict())
        self_dict[AttributeNames.FILTERING_CONTEXTS.value] = filtering_context

        return self_dict

    class DataAppEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, (DataApp, Widget)):
                return o.to_dict_widget()
            try:
                return o.__dict__
            except AttributeError as attr_error:
                print(f"ERROR: {attr_error}")
                return {}

    def to_json(self):
        """
        Shows your dataApp specification in JSON format.
        """
        return json.dumps(self, cls=DataApp.DataAppEncoder, indent=2)

    def __repr__(self):
        s_repr = f"{AttributeNames.NAME.value}={self.name}, "
        s_repr += f"{AttributeNames.DESCRIPTION.value}={self.description}, "
        s_repr += f"{AttributeNames.VERSION.value}={self.version}, "
        s_repr += f"{AttributeNames.TAGS.value}={self.tags}"
        return s_repr
