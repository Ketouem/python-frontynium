from frontynium.exceptions import ObjectMappingNotFound, InvalidObjectMapping
from frontynium.finder import Finder, ExpressionBuilder
from types import FunctionType


class Page(object):

    def __init__(self, root_node):
        """Default constructor

        root_node -- instance of selenium's webdriver or webelement
        """
        self._root_node = root_node
        self._finder = Finder(self._root_node)
        self._objects = {}
        for obj in self._objects:
            if not isinstance(obj, ExpressionBuilder):
                raise InvalidObjectMapping("You must use the methods available in the finder.")

    #Preventing a var = Page(webdriver) in a test code as _objects needs to be defined correctly
    def __new__(cls, *args, **kwargs):
        if cls is Page:
            raise TypeError("This class is not meant to be instantiated directly but subclassed")
        return object.__new__(cls, *args, **kwargs)

    def _find_objects(self, object_name, single_element=False, *args, **kwargs):
        element = None
        try:
            mapping = self._objects[object_name].build()
            if type(mapping) == FunctionType:
                element = mapping(single_element, *args, **kwargs)
        except KeyError:
            raise ObjectMappingNotFound("Object {0} has not been found in the objects dictionary.".format(object_name))
        return element

    def click_on(self, object_name, *args, **kwargs):
        element = self._find_objects(object_name, *args, **kwargs)
        element.click()
        return self

    def set_field(self, object_name, value, clear_before_use=False, *args, **kwargs):
        element = self._find_objects(object_name, *args, **kwargs)
        if clear_before_use:
            element.clear()
        element.send_keys(value)
        return self

    @property
    def root_node(self):
        return self._root_node

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, value):
        self._objects = value


#Page decorators


def gettable(*args):
    def wrapper(wrapped_class):
        if not isinstance(wrapped_class, Page):
            raise ValueError("The gettable decorator must be use on a Page class only.")
        for arg in args:
            getter = lambda current_instance: current_instance._find_objects(arg)
            setattr(wrapped_class, 'get_' + arg, getter)
        return wrapped_class
    return wrapper


def settable(*args):
    def wrapper(wrapped_class):
        if not isinstance(wrapped_class, Page):
            raise ValueError("The settable decorator must be use on a Page class only.")
        for arg in args:
            def setter(current_instance, value, clear=False, *opts, **kopts):
                return current_instance.set_field(arg, value, clear, *opts, **kopts)
            setattr(wrapped_class, 'set_' + arg, setter)
        return wrapped_class
    return wrapper