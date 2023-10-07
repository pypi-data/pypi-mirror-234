from __future__ import annotations

from ..widget import AttributeNames, Widget


class Button(Widget):
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

    def __init__(self,
                 text_button: str = None,
                 **additional):
        Widget.__init__(self, self.__class__.__name__,
                        compatibility=tuple([Button.__name__, str.__name__, int.__name__, float.__name__]),
                        **additional)
        self._parent_class = Button.__name__
        self.text = text_button

    def from_string(self, string: str) -> Button:
        self.text = string
        return self

    def from_int(self, number: int) -> Button:
        self.text = str(number)
        return self

    def from_float(self, number: float) -> Button:
        self.text = str(number)
        return self

    def to_dict_widget(self):
        button_dict = super().to_dict_widget()
        _widget_providers = []
        if self.text is not None:
            if isinstance(self.text, str):
                button_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT.value: self.text,
                })
            elif isinstance(self.text, Widget):
                target = {"id": self.text.widget_id, "target": AttributeNames.TEXT.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Text value should be a string or another widget")

        if _widget_providers:
            self.add_widget_providers(button_dict, _widget_providers)

        return button_dict
