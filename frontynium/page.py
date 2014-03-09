from frontynium.exceptions import ObjectMappingNotFound, InvalidObjectMapping
from frontynium.finder import Finder, ExpressionBuilder
from types import FunctionType


class Page(object):

    def __init__(self, root_node):
        """Default constructor

        :param root_node: instance of selenium's webdriver or webelement
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
            raise TypeError("This class is not meant to be instantiated directly but subclassed.")
        return object.__new__(cls, *args, **kwargs)

    def detect_objects(self, object_name, *args, **kwargs):
        """Trigger the detection of objects

        :param object_name: the name of the mapping as defined in self._objects
        :returns WebElement or list<WebElement>
        """
        element = None
        try:
            mapping = self._objects[object_name].build()
            if type(mapping) == FunctionType:
                element = mapping(*args, **kwargs)
        except KeyError:
            raise ObjectMappingNotFound("Object {0} has not been found in the objects dictionary.".format(object_name))
        return element

    def click_on(self, object_name, *args, **kwargs):
        """Click on an object defined in _objects

        :param object_name: the name of the mapping as defined in self._objects
        :returns the current instance of Page
        """
        element = self.detect_objects(object_name, *args, **kwargs)
        element.click()
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


def gettable(*args):
    def inner(cls):
        for arg in args:
            def getter(cls, *sargs, **skwargs):
                return cls.detect_objects(arg, *sargs, **skwargs)
            setattr(cls, 'get_' + arg, getter)
        return cls
    return inner


def settable(*args):
    def inner(cls):
        for arg in args:
            def setter(cls, value, clear_before_use=False, *sargs, **skwargs):
                obj = cls.detect_objects(arg, *sargs, **skwargs)[0]
                if clear_before_use:
                    obj.clear()
                obj.send_keys(value)
                return cls
            setattr(cls, 'set_' + arg, setter)
        return cls
    return inner

def clickable():
    pass