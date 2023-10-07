from __future__ import annotations

import base64
import uuid

from dataclasses import dataclass
from io import BytesIO
from matplotlib.figure import Figure
from pathlib import Path
from typing import Union, Tuple, Optional

from os.path import isfile as file_exists
from ..widget import Widget, AttributeNames, StateControl


@dataclass
class Image(StateControl):
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
    img: Optional[Union[str, bytes, Path, Figure]] = None
    caption: Optional[str] = None
    placeholder: Optional[Union[str, bytes, Path]] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Image):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.img = new_widget.img
        self.caption = new_widget.caption
        self.placeholder = new_widget.placeholder

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.img is not None:
            return self.img
        return None

    def from_figure(self, fig: Figure):
        self.img = fig
        return self

    def to_figure(self):
        return self.img

    def to_dict_widget(self, image_dict: dict = None):
        if image_dict is None:
            image_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Image.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []
        if self.img is not None:
            if isinstance(self.img, str):
                # Reading image from local PATH
                if file_exists(self.img):
                    with open(self.img, 'rb') as file:
                        buffer = file.read()
                        image_data = base64.b64encode(buffer).decode('utf-8')

                    image_dict[AttributeNames.PROPERTIES.value].update(
                        {AttributeNames.DATA.value: f"{image_data}"}
                    )
                else:
                    raise FileNotFoundError(f"The file {self.img} does not exist")
            elif isinstance(self.img, Path):
                if self.img.exists():
                    with open(self.img, 'rb') as file:
                        buffer = file.read()
                        image_data = base64.b64encode(buffer).decode('utf-8')

                    image_dict[AttributeNames.PROPERTIES.value].update(
                        {AttributeNames.DATA.value: f"{image_data}"}
                    )
                else:
                    raise FileNotFoundError(f"The file {self.img} does not exist")
            elif isinstance(self.img, bytes):
                image_data = base64.b64encode(self.img).decode("utf-8")

                image_dict[AttributeNames.PROPERTIES.value].update(
                    {AttributeNames.DATA.value: f"{image_data}"}
                )
            elif isinstance(self.img, Figure):
                bio = BytesIO()
                # TODO: pass information from self._additional to savefig function
                self.img.savefig(bio, format="png", bbox_inches='tight')
                image_data = base64.b64encode(bio.getvalue()).decode("utf-8")

                image_dict[AttributeNames.PROPERTIES.value].update(
                    {AttributeNames.DATA.value: f"{image_data}"}
                )
            elif isinstance(self.img, Widget):
                target = {"id": self.img.widget_id, "target": "img"}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Image value not allow")

        if self.placeholder is None:
            currentDirectory = Path(__file__).parent.resolve()
            dataDirectory = currentDirectory.joinpath("resources")
            placeholder_img = dataDirectory / "placeholder.jpg"
            self.placeholder = placeholder_img

        if isinstance(self.placeholder, str):
            # Reading image from local PATH
            if file_exists(self.placeholder):
                with open(self.placeholder, 'rb') as file:
                    buffer = file.read()
                    image_data = base64.b64encode(buffer).decode('utf-8')

                image_dict[AttributeNames.PROPERTIES.value].update(
                    {AttributeNames.PLACEHOLDER.value: f"{image_data}"}
                )
            else:
                raise FileNotFoundError(f"The file {self.placeholder} does not exist")
        elif isinstance(self.placeholder, Path):
            if self.placeholder.exists():
                with open(self.placeholder, 'rb') as file:
                    buffer = file.read()
                    image_data = base64.b64encode(buffer).decode('utf-8')

                image_dict[AttributeNames.PROPERTIES.value].update(
                    {AttributeNames.PLACEHOLDER.value: f"{image_data}"}
                )
            else:
                raise FileNotFoundError(f"The file {self.placeholder} does not exist")
        elif isinstance(self.placeholder, bytes):
            image_data = base64.b64encode(self.placeholder).decode("utf-8")

            image_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.PLACEHOLDER.value: f"{image_data}"}
            )

        if self.caption is not None:
            if isinstance(self.caption, str):
                image_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.CAPTION.value: self.caption
                })
            elif isinstance(self.caption, Widget):
                target = {"id": self.caption.widget_id, "target": "caption"}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Caption value should be a string or another widget")

        if _widget_providers:
            self.add_widget_providers(image_dict, _widget_providers)

        return image_dict


class ImageWidget(Image, Widget):
    def __init__(self,
                 img: Optional[Union[str, bytes, Path, Figure]] = None,
                 caption: Optional[str] = None,
                 placeholder: Optional[Union[str, bytes, Path]] = None,
                 **additional):
        Widget.__init__(self, Image.__name__,
                        compatibility=tuple([str.__name__, bytes.__name__, Path.__name__,
                                            Figure.__name__, Image.__name__]),
                        **additional)
        Image.__init__(self, img=img, caption=caption, placeholder=placeholder)
        self._parent_class = Image.__name__

    def to_dict_widget(self):
        image_dict = Widget.to_dict_widget(self)
        image_dict = Image.to_dict_widget(self, image_dict)
        return image_dict
