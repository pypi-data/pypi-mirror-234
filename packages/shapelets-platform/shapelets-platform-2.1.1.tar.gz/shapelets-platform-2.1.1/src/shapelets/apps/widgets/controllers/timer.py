from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from ..widget import Widget, AttributeNames, StateControl


@dataclass
class Timer(StateControl):
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

    Returns
    -------
    Timer

    Examples
    --------
    >>> timer = app.timer(title="Timer", every=1.0, times=10)         


    """
    title: Optional[str] = None
    every: Optional[Union[int, float]] = None
    start_delay: Optional[int] = None
    times: Optional[int] = None
    hidden: Optional[bool] = False
    start_on_init: Optional[bool] = False

    def from_string(self, string: str) -> Timer:
        self.title = string
        return self

    def to_string(self) -> str:
        return str(self.every)

    def from_int(self, number: int) -> Timer:
        self.every = number
        return self

    def to_int(self) -> int:
        return int(self.every)


class TimerWidget(Widget, Timer):
    def __init__(self,
                 title: str = None,
                 every: Union[int, float] = None,
                 start_delay: Optional[int] = None,
                 times: Optional[int] = None,
                 hidden: Optional[bool] = False,
                 start_on_init: Optional[bool] = False,
                 **additional):
        Widget.__init__(self, Timer.__name__,
                        compatibility=tuple([str.__name__, int.__name__, float.__name__, Timer.__name__]),
                        **additional)
        Timer.__init__(self, title=title, every=every, start_delay=start_delay, times=times, hidden=hidden, start_on_init=start_on_init)
        self._parent_class = Timer.__name__

    def to_dict_widget(self):
        timer_dict = super().to_dict_widget()
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.title is not None:
            if isinstance(self.title, str):
                timer_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.every is not None:
            if isinstance(self.every, (int, float)):
                timer_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.EVERY.value: self.every
                })
            elif isinstance(self.every, Widget):
                target = {"id": self.every.widget_id, "target": AttributeNames.EVERY.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Every value should be a int or another widget")

        if self.start_delay is not None:
            if isinstance(self.start_delay, int):
                timer_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.START_DELAY.value: self.start_delay
                })
            elif isinstance(self.start_delay, Widget):
                target = {"id": self.start_delay.widget_id, "target": AttributeNames.START_DELAY.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Start Delay value should be a int or another widget")

        if self.times is not None:
            if isinstance(self.times, int):
                timer_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TIMES.value: self.times
                })
            elif isinstance(self.times, Widget):
                target = {"id": self.times.widget_id, "target": AttributeNames.TIMES.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Times value should be a int or another widget")

        if self.hidden is not None:
            if isinstance(self.hidden, bool):
                timer_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.HIDDEN.value: self.hidden
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Hidden value should be a boolean")

        if self.start_on_init is not None:
            if isinstance(self.start_on_init, bool):
                timer_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.START_ON_INIT.value: self.start_on_init
                })
            else:
                raise ValueError(f"Error Widget {self.widget_type}: start_on_init value should be a boolean")

        if _widget_providers:
            self.add_widget_providers(timer_dict, _widget_providers)

        return timer_dict

    @staticmethod
    def bind():
        raise AttributeError("Button widget does not allow bind")
