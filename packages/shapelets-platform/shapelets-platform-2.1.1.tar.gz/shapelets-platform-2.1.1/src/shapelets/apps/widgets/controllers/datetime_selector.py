from __future__ import annotations

import uuid

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional, Union, Dict

from ..widget import AttributeNames, StateControl, Widget
from ..datetime_utils import _date_to_string, _transform_date_time_value


@dataclass
class DateSelector(StateControl):
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
    title: Optional[str] = None
    date_time: Optional[Union[float, int, str, datetime, date, time]] = None
    min_date: Optional[Union[float, int, str, date]] = None
    max_date: Optional[Union[float, int, str, date]] = None
    _format: Optional[str] = None
    _date_time_str = None
    _min_date_str = None
    _max_date_str = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

        if self.date_time is not None:
            self._date_time_str, self._format = _transform_date_time_value(self.date_time)

        if self.min_date is not None:
            try:
                self._min_date_str = _date_to_string(self.min_date)
            except:
                raise ValueError(f"Unexpected type {type(self.min_date)} for min_date.")

        if self.max_date is not None:
            try:
                self._max_date_str = _date_to_string(self.max_date)
            except:
                raise ValueError(f"Unexpected type {type(self.max_date)} for max_date.")

    def replace_widget(self, new_widget: DateSelector):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.title = new_widget.title
        self.date_time = new_widget.date_time
        self.min_date = new_widget.min_date
        self.max_date = new_widget.max_date
        self._format = new_widget._format
        self._date_time_str = new_widget._date_time_str
        self._min_date_str = new_widget._min_date_str
        self._max_date_str = new_widget._max_date_str

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.date_time is not None:
            return self.date_time
        return None

    def from_datetime(self, dt: datetime) -> DateSelector:
        self.date_time = dt
        return self

    def from_date(self, dt: date) -> DateSelector:
        self.date_time = dt
        return self

    def from_time(self, dt: time) -> DateSelector:
        self.date_time = dt
        return self

    def from_string(self, dt: str) -> DateSelector:
        self._date_time_str, self._format = _transform_date_time_value(dt)
        return dt

    def to_string(self) -> str:
        if isinstance(self.date_time, str):
            return self.date_time

        if isinstance(self.date_time, datetime):
            date_str = self.date_time.strftime("%Y-%m-%d, %H:%M:%S")
            return date_str

        if isinstance(self.date_time, date):
            date_str = self.date_time.strftime("%Y-%m-%d")
            return date_str

        if isinstance(self.date_time, time):
            date_str = self.date_time.strftime("%H:%M:%S")
            return date_str

        return self._date_time_str

    def to_datetime(self) -> datetime:
        if isinstance(self.date_time, datetime):
            return self.date_time

    def to_date(self) -> date:
        if isinstance(self.date_time, datetime):
            try:
                dt = datetime.strptime(self.date_time, '%Y-%m-%d').date()
                return dt
            except:
                return None

        elif isinstance(self.date_time, date):
            return self.date_time

        else:
            return None

    def to_dict_widget(self, date_dict: Dict = None) -> Dict:
        if date_dict is None:
            date_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: DateSelector.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.date_time is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VALUE.value: self._date_time_str,
            })

            if self._format is not None:
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.FORMAT.value: self._format
                })

        if self.min_date is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.MIN_DATE.value: self._min_date_str
            })

        if self.max_date is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.MAX_DATE.value: self._max_date_str
            })

        if _widget_providers:
            self.add_widget_providers(date_dict, _widget_providers)

        return date_dict


class DateSelectorWidget(DateSelector, Widget):

    def __init__(self,
                 title: Optional[str] = None,
                 date_time: Optional[Union[float, int, str, datetime, date, time]] = None,
                 min_date: Optional[Union[float, int, str, date]] = None,
                 max_date: Optional[Union[float, int, str, date]] = None,
                 **additional):
        Widget.__init__(self, DateSelector.__name__,
                        compatibility=tuple(
                            [
                                DateSelector.__name__,
                                float.__name__,
                                str.__name__,
                                datetime.__name__,
                                date.__name__,
                                time.__name__
                            ]
                        ),
                        **additional)
        DateSelector.__init__(self, title=title, date_time=date_time, min_date=min_date, max_date=max_date)

        self._parent_class = DateSelector.__name__

    def to_dict_widget(self) -> Dict:
        date_dict = Widget.to_dict_widget(self)
        date_dict = DateSelector.to_dict_widget(self, date_dict)
        return date_dict
