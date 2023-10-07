from __future__ import annotations

import base64
import dill
import inspect
import uuid
import zlib

from dataclasses import dataclass
from typing import Callable, overload, Union, List, Dict, Tuple
from typing_extensions import get_args

from .attribute_names import AttributeNames

import __main__
import sys


class Widget:
    """
    Units defined in Layout
    """

    def __init__(self,
                 widget_type: str,
                 widget_id: str = None,
                 draggable: bool = False,
                 resizable: bool = False,
                 # these are the optional properties:
                 placeholder: str = None,
                 disabled: bool = None,
                 compatibility: tuple = None,
                 parent_data_app: object = None) -> object:
        # parent_data_app is a reference to the DataApp used as a factory
        # for this widget
        self.parent_data_app = parent_data_app
        self.widget_id = widget_id if widget_id else str(uuid.uuid1())
        self.widget_type = widget_type
        self.placeholder = placeholder
        self.disabled = disabled
        self.draggable = draggable
        self.resizable = resizable
        self._bind = []
        self._mainlist = []
        self._inspectedlist = []
        self._compatibility = compatibility
        self._caller = None

    @property
    def widget_compatibility(self):
        return list(self._compatibility)

    def to_dict_widget(self):
        properties = {}
        if self.placeholder is not None:
            properties[AttributeNames.PLACEHOLDER.value] = self.placeholder
        widget_dict = {
            AttributeNames.ID.value: self.widget_id,
            AttributeNames.TYPE.value: self.widget_type,
            AttributeNames.DRAGGABLE.value: self.draggable,
            AttributeNames.RESIZABLE.value: self.resizable,
            AttributeNames.DISABLED.value: False if self.disabled is None else self.disabled,
            AttributeNames.BIND.value: self._bind if self._bind else None,
            AttributeNames.PROPERTIES.value: properties
        }
        return widget_dict

    @staticmethod
    def add_widget_providers(current_dict: dict, providers: dict):
        """
        When any attribute from a widget receives another widget inside, this widget is called a provider. This means
        that the widget attribute with the provider inside must update its value everytime the provider changes.
        In order to do this, a list of providers is given to the UI. This list contains the id of the provider widget
        and the target attribute of the current widget. This list looks like:
        providers: [{
                      id: 85535b68-2dce-11ed-bd74-00155d7482db,
                      target: title
                     }]
        The list of providers is added to the bind section of the current widget.
        """
        if current_dict[AttributeNames.BIND.value]:
            current_dict[AttributeNames.BIND.value].append({
                "providers": providers
            })
        else:
            current_dict[AttributeNames.BIND.value] = [
                {"providers": providers}
            ]

    @overload
    def bind(self, string: str):
        ...

    @overload
    def bind(self, fn: Callable, *args, **kwargs):
        ...

    def bind(self, fn: Union[Callable, str], *args, **kwargs):
        if isinstance(fn, Callable):
            self._bind_function(fn, *args, **kwargs)
        if isinstance(fn, str):
            self._add_bind_to_widget(props=fn)

    @staticmethod
    def _is_last_level(fn):
        last = True
        for attribute in list(fn.__globals__.keys()):
            if not attribute.startswith('__'):
                f = fn.__globals__[attribute]
                if inspect.isfunction(f) and f.__name__ != fn.__name__:
                    last = False
                    break

        return last

    def _mainify_functions(self, fn):
        """
        This method searchs for functions not defined in __main__ and 'mainify' them
        It is used for server side functions in order to serialize properly all the functions,
        even those not included in the main file
        """
        for attribute in list(fn.__globals__.keys()):
            if not attribute.startswith('__'):
                f = fn.__globals__[attribute]
                if inspect.isfunction(
                        f) and f.__name__ != fn.__name__ and f.__name__ not in self._inspectedlist and hasattr(f,
                                                                                                               '__module__'):
                    if f.__module__ is not None:
                        module = __import__(f.__module__)
                        if 'lib/python' not in module.__file__:
                            self._inspectedlist.append(f.__name__)
                            if (f.__name__ not in self._mainlist):
                                self._mainify(f)
                                self._mainlist.append(f.__name__)

                            if not self._is_last_level(f):
                                self._mainify_functions(f)

    @staticmethod
    def _mainify(obj):
        """
        If obj is not defined in __main__ then redefine it in 
        main so that dill will serialize the definition along with the object
        """
        if obj.__module__ != "__main__":
            obj.__module__ = "__main__"
            obj.__globals__["__module__"] = "__main__"

            try:
                s = inspect.getsource(obj)
            except:
                print(f"Not possible to get source from function {obj.__name__}")
                return

            try:
                co = compile(s.lstrip(), '<string>', 'exec')
            except:
                print(f"Not possible to compile source from function {obj.__name__}")
                return

            try:
                exec(co, __main__.__dict__)
            except:
                print(f"Not possible to execute the given source from function {obj.__name__}")
                return

    def _bind_function(self, fn: Callable, *args, **kwargs):
        """
        Bind for functions
        """
        self._caller = f"{sys._getframe(2).f_code.co_filename}"
        self._mainify_functions(fn)

        try:
            return_type = fn.__annotations__['return'].__name__
        except AttributeError:
            return_type = fn.__annotations__['return']._name

        if return_type == "List" and get_args(fn.__annotations__['return']):
            # If return type is a list, it might contain another type inside
            inside_type = get_args(fn.__annotations__['return'])[0].__name__
            if inside_type == "Sequence" or inside_type == "View":
                # For now, let's care only if the inside type is a Sequence or View
                return_type = f"{return_type}[{inside_type}]"

        fn_original_name = fn.__name__
        if return_type in self._compatibility:
            entry_arguments = self._find_parameters(fn)
            # Find other widgets references' inside the function
            references = []

            if len(args) > len(entry_arguments):
                raise TypeError(
                    "Function %s called with incorrectly specified arguments. Expected %i but received %i" % (
                        fn_original_name, len(entry_arguments), len(args)))

            on_changes_widgets = []
            mute_widgets = []

            empty_mute = False if "mute" in kwargs else True

            for i, arguments in enumerate(args):
                if isinstance(arguments, list):
                    # If user provides with a list, check if there are widgets inside.
                    # User could provide mixed types : [widget, str, widget, int].
                    # When a list is provided, widgets inside are also triggers.
                    ref_ids = []
                    for item_in_list in arguments:
                        if isinstance(item_in_list, Widget):
                            if empty_mute:
                                on_changes_widgets.append(item_in_list.widget_id)
                            else:
                                mute_widgets.append(item_in_list.widget_id) if item_in_list in kwargs.get(
                                    "mute") else on_changes_widgets.append(item_in_list.widget_id)
                            ref_ids.append(item_in_list.widget_id)
                        else:
                            # Regular Value
                            ref_ids.append(item_in_list)
                    references.append(
                        {
                            "ref": ref_ids,
                            "name": entry_arguments[i]["name"],
                            "type": entry_arguments[i]["type"],
                        }
                    )

                elif isinstance(arguments, Widget):
                    if empty_mute:
                        on_changes_widgets.append(arguments.widget_id)
                    else:
                        mute_widgets.append(arguments.widget_id) if arguments in kwargs.get(
                            "mute") else on_changes_widgets.append(arguments.widget_id)

                    references.append(
                        {
                            "ref": arguments.widget_id,
                            "name": entry_arguments[i]["name"],
                            "type": entry_arguments[i]["type"],
                            "default": entry_arguments[i]["default"],
                        }
                    )
                else:
                    references.append(
                        {
                            "value": str(base64.b64encode(dill.dumps(arguments, recurse=True)), encoding='utf-8'),
                            "name": entry_arguments[i]["name"],
                            "type": entry_arguments[i]["type"],
                            "default": entry_arguments[i]["default"],
                            "pickled": True
                        }
                    )

            # Get widgets from Triggers
            triggers = self._find_triggers(kwargs)
            on_changes_widgets.extend(triggers)
            # Get widgets defined as triggers and mute at the same time
            wrong_widgets = self._intersection(mute_widgets, on_changes_widgets)
            # Get only well defined triggers
            on_changes_widgets = [trigger for trigger in on_changes_widgets if trigger not in wrong_widgets]

            # We need to check if there is another function already in the bind attribute in order to avoid looping with triggers
            if on_changes_widgets and len(self._bind) > 0:
                self._check_triggers(on_changes_widgets)
            # Adjust entry arguments
            fn = self._adjust_arguments(fn, entry_arguments)

            body = fn
            if return_type != self._parent_class:
                # If the return type is not a widget, we need to adjust the return type.
                body = self._adjust_return(fn, return_type)

            # Function are saved  with a unique id, so the function won't be replaced when it is used multiple times.
            # This is because when a basic type is returned like str or int, the return value will only change the
            # value of the widget, but we want to keep the other widget attributes like the title.
            # If we don't use unique functions for each widget, we won't be able to keep the other attributes.
            fn_uid = str(uuid.uuid1())
            # Add to Widget Structure
            self._add_bind_to_widget(fn=fn_uid, result=self._parent_class,
                                     parameters=references, triggers=on_changes_widgets)
            # Serialize function.
            ser_body = base64.b64encode(zlib.compress(dill.dumps(body, recurse=True))).decode('utf-8')
            result = {
                "body": fn_uid,
                "parameters": entry_arguments,
                "result": self._parent_class,
                "ser_body": ser_body
            }
            # Add to DataApp Structure with function uid
            self.parent_data_app.functions[fn_uid] = result
            # Append fn uid to dataApp data to keep track of what files belong to each dataApp.
            try:
                # If this bind ins happening inside a custom function, there is no access to the dataApp, therefore
                # insert the information into the database.
                self.parent_data_app._update_data([fn_uid])
            except Exception:
                # If the previous call fails, It means the dataApp is not yet created, and therefor we add the information
                # to the _data attribute, which will be added to the database once the dataApp is registered.
                self.parent_data_app._data.append(fn_uid)

            if kwargs.get("on_init"):
                try:
                    self._prepare_execution_on_registration(args, body)
                except Exception as e:
                    # Continue with the dataApp registration although on_init execution could not be completed.
                    pass

        else:
            raise ValueError("Return type does not match")

    def _prepare_execution_on_registration(self, input_args: Tuple, fn_body: Callable):
        """
        Execute bind function on dataApp registration
        param input_args: args to use in the function
        param fn_body: function to be executed.

        The result will replace the values inside the bind widget.
        """
        input_values = []
        for item in input_args:
            if isinstance(item, Widget):
                widget_value = item.get_current_value()
                if widget_value is not None:
                    input_values.append(widget_value)
                else:
                    raise ValueError(f"Pre-execution cannot be completed. {item.widget_type} has no value")
            else:
                input_values.append(item)
        result = fn_body(*input_values)
        self.replace_widget(result)

    @staticmethod
    def _intersection(lst1, lst2) -> List:
        return list(set(lst1) & set(lst2))

    @staticmethod
    def _find_parameters(fn: Callable) -> List:
        """
        Find the parameters use in a function.
        param fn: Function to extract parameters from.
        return List with all the parameters.
        """
        parameters = []
        for param in inspect.signature(fn).parameters.values():
            try:
                input_type = param.annotation.__name__
            except AttributeError:
                # When using typing, type name is included in _name
                input_type = param.annotation._name
            parameters.append({
                "name": param.name,
                "type": input_type,
                "default": None if param.default is param.empty else param.default
            })
        return parameters

    @staticmethod
    def _find_triggers(kwargs: Dict) -> List:
        """
        Find if there are triggers in the kwargs. In bind function, triggers are defined in the triggers parameter.
        param kwargs.
        return List of all the triggers.
        """
        triggers = []
        if kwargs.get("triggers"):
            triggers = [y.widget_id for y in kwargs.get("triggers")]
        return triggers

    def _add_bind_to_widget(self,
                            fn: str = None,
                            result: str = None,
                            props: str = None,
                            parameters: List = None,
                            triggers: List = None):
        """
        Find if there are triggers to bind in the kwargs. In bind function, triggers are defined in the triggers parameter.
        param fn_name: Name of the function or uid to add.
        param props: Properties to change.
        param parameters: Parameters use in the function.
        param triggers: Widgets that trigger the bind.
        """
        self._bind.append({
            "fn": fn,
            "result": result,
            "props": props,
            "parameters": parameters,
            "triggers": triggers
        })

    def _adjust_return(self, fn: Callable, return_type) -> Callable:
        """
        Add wrapper to function in order to return a Widget.
        If the return value type of the function (fn) is different from the widget type that will receive this result,
        but compatible with the value of the widget, we will wrap the function result to return the same widget type
        with the result inside. Therefore, the front-end will send the function to the back-end to be executed,
        without worrying about the return type since it will always be a compatible widget. When registering the DataApp,
        if the widget does not support the return type, an exception is raised.
        param fn: function to wrap.
        param return_type: return type from the function.
        return new function with return type wrapped
        """
        if return_type == "str":
            if "from_string" not in dir(self):
                raise Exception("String return type not supported for this widget")

            def result_from_string(*args, **kwargs) -> Widget:
                return self.from_string(fn(*args, **kwargs))

            return result_from_string
        elif return_type == "int":
            if "from_int" not in dir(self):
                raise Exception("Int return type not supported for this widget")

            def result_from_int(*args, **kwargs) -> Widget:
                return self.from_int(fn(*args, **kwargs))

            return result_from_int
        elif return_type == "float":
            if "from_float" not in dir(self):
                raise Exception("Float return type not supported for this widget")

            def result_from_float(*args, **kwargs) -> Widget:
                return self.from_float(fn(*args, **kwargs))

            return result_from_float
        elif return_type == "bool":
            if "from_bool" not in dir(self):
                raise Exception("Boolean return type not supported for this widget")

            def result_from_bool(*args, **kwargs) -> Widget:
                return self.from_bool(fn(*args, **kwargs))

            return result_from_bool
        elif return_type == "DataFrame":
            if "from_dataframe" not in dir(self):
                raise Exception("DataFrame return type not supported for this widget")

            def result_from_dataframe(*args, **kwargs) -> Widget:
                return self.from_dataframe(fn(*args, **kwargs))

            return result_from_dataframe
        elif return_type == "ndarray":
            if "from_ndarray" not in dir(self):
                raise Exception("ndarray return type not supported for this widget")

            def result_from_ndarray(*args, **kwargs) -> Widget:
                return self.from_ndarray(fn(*args, **kwargs))

            return result_from_ndarray
        elif return_type == "list":
            if "from_list" not in dir(self):
                raise Exception("list return type not supported for this widget")

            def result_from_list(*args, **kwargs) -> Widget:
                return self.from_list(fn(*args, **kwargs))

            return result_from_list
        elif return_type == "List":
            if "from_List" not in dir(self):
                raise Exception("List return type not supported for this widget")

            def result_from_List(*args, **kwargs) -> Widget:
                return self.from_list(fn(*args, **kwargs))

            return result_from_List
        elif return_type == "Colors":
            if "from_color" not in dir(self):
                raise Exception("Color return type not supported for this widget")

            def result_from_color(*args, **kwargs) -> Widget:
                return self.from_color(fn(*args, **kwargs))

            return result_from_color
        elif return_type == "Sequence":
            if "from_sequence" not in dir(self):
                raise Exception("Sequence return type not supported for this widget")

            def result_from_sequence(*args, **kwargs) -> Widget:
                return self.from_sequence(fn(*args, **kwargs))

            return result_from_sequence
        elif return_type == "View":
            if "from_view" not in dir(self):
                raise Exception("View return type not supported for this widget")

            def result_from_view(*args, **kwargs) -> Widget:
                return self.from_view(fn(*args, **kwargs))

            return result_from_view
        elif return_type == "List[View]":
            if "from_views" not in dir(self):
                raise Exception("List of Views return type not supported for this widget")

            def result_from_views(*args, **kwargs) -> Widget:
                return self.from_views(fn(*args, **kwargs))

            return result_from_views
        elif return_type == "List[Sequence]":
            if "from_sequences" not in dir(self):
                raise Exception("List of Views return type not supported for this widget")

            def result_from_sequences(*args, **kwargs) -> Widget:
                return self.from_sequences(fn(*args, **kwargs))

            return result_from_sequences
        elif return_type == "datetime":
            if "from_datetime" not in dir(self):
                raise Exception("datetime return type not supported for this widget")

            def result_from_datetime(*args, **kwargs) -> Widget:
                return self.from_datetime(fn(*args, **kwargs))

            return result_from_datetime
        elif return_type == "date":
            if "from_date" not in dir(self):
                raise Exception("date return type not supported for this widget")

            def result_from_date(*args, **kwargs) -> Widget:
                return self.from_date(fn(*args, **kwargs))

            return result_from_date
        elif return_type == "time":
            if "from_time" not in dir(self):
                raise Exception("time return type not supported for this widget")

            def result_from_time(*args, **kwargs) -> Widget:
                return self.from_time(fn(*args, **kwargs))

            return result_from_time
        elif return_type == "Series":
            if "from_series" not in dir(self):
                raise Exception("Series return type not supported for this widget")

            def result_from_series(*args, **kwargs) -> Widget:
                return self.from_series(fn(*args, **kwargs))

            return result_from_series
        elif return_type == "Figure":
            if "from_figure" not in dir(self):
                raise Exception("Figure return type not supported for this widget")

            def result_from_figure(*args, **kwargs) -> Widget:
                return self.from_figure(fn(*args, **kwargs))

            return result_from_figure
        elif return_type == "DataSet":
            if "from_dataset" not in dir(self):
                raise Exception("Figure return type not supported for this widget")

            def result_from_dataset(*args, **kwargs) -> Widget:
                return self.from_dataset(fn(*args, **kwargs))

            return result_from_dataset
        else:
            raise Exception(f"Return type {return_type} not supported for this widget")

    @staticmethod
    def _adjust_arguments(fn: Callable, references: List) -> Callable:
        """
        Add Wrapper to arguments to use the requested type.
        When a function requests any Python native type, but a widget is given, we wrap the function arguments
        to extract the value of the given widget and convert it to the requested type. This allows for the execution
        to be carried out quickly and easily, as all the work is done before actually executing the function.
        param fn: function to wrap.
        param references: List of arguments use in the function. Contains the widget reference, type, etc.
        return new function with entry arguments wrapped to use the proper types.
        """
        type_list = []
        for argument in references:
            type_list.append(argument["type"])

        def fun_new_arguments(*args, **kwargs):
            new_args = []
            for i, item in enumerate(args):
                if isinstance(item, Widget):
                    argument_type = type_list[i]
                    if argument_type == "str":
                        new_args.append(item.to_string())
                    elif argument_type == "int":
                        new_args.append(item.to_int())
                    elif argument_type == "float":
                        new_args.append(item.to_float())
                    else:
                        new_args.append(item.value)
                else:
                    argument_type = type_list[i]
                    if argument_type == "str":
                        new_args.append(str(item))
                    elif argument_type == "int":
                        new_args.append(int(item))
                    elif argument_type == "float":
                        new_args.append(float(item))
                    else:
                        new_args.append(item)
            return fn(*new_args)

        return fun_new_arguments

    def _check_triggers(self, triggers):
        for fn in self._bind:
            for param in fn["triggers"]:
                if param in triggers:
                    raise Exception(f"Trigger Loop Found")


@dataclass
class StateControl:
    disabled: bool = False
    draggable: bool = False
    resizable: bool = False
    placeholder: str = None
