from frontynium.exceptions import ObjectMappingNotFound, InvalidObjectMapping
from frontynium.finder import Finder, ExpressionBuilder
from types import FunctionType


class Page(object):
    """Implementation of the PageObject Pattern (https://code.google.com/p/selenium/wiki/PageObjects)

    This class provides tools that are useful to manipulate a web UI using selenium. This class is not meant
    to be used directly but being subclassed.

    Ex:

    class MyAwesomePage(Page):

        def __init___(self, webdriver):
            Page.__init__(self, webdriver)

            #In this dictionary we will put all the mapping for the controls, eg a sample name and the detection
            #mean.
            self._mapped_objects = {
                'input': self._finder.by_css("input#test-123")
                'validate_button': self._finder.by_css("div.button")
            }

        def search_data(self, value):


    """
    def __init__(self, root_node):
        """Default constructor

        :param root_node: instance of selenium's webdriver or webelement
        """
        self._root_node = root_node
        self._finder = Finder(self._root_node)
        self._mapped_objects = {}
        for obj in self._mapped_objects:
            if not isinstance(obj, ExpressionBuilder):
                raise InvalidObjectMapping("You must use the methods available in the finder.")

    #Preventing a var = Page(webdriver) in a test code as _mapped_objects needs to be defined correctly
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
            mapping = self._mapped_objects[object_name].build()
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

    def set_value_into(self, object_name, value, clear_before_use=False, *args, **kwargs):
        """Set a value into a mapped field

        :param object_name: the name of the mapping as defined in self._objects
        :param value: the string that will be input into the control
        :param clear_before_use: empty the field before use
        :returns the current instance of Page
        """
        element = self.detect_objects(object_name, *args, **kwargs)
        if type(element) == list:
            element = element[0]
        if clear_before_use:
            element.clear()
        element.send_keys(value)
        return self

    @property
    def root_node(self):
        return self._root_node

    @property
    def objects(self):
        return self._mapped_objects

    @objects.setter
    def objects(self, value):
        self._mapped_objects = value


def gettable(*args):
    """Decorator that allows the creation of getter functions to expose the WebElement(s)

    :param *args: str, each str being the name of a mapping inside Page._mapped_objects
    """
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
                obj = cls.detect_objects(arg, *sargs, **skwargs)
                if type(obj) == list:
                    obj = obj[0]
                if clear_before_use:
                    obj.clear()
                obj.send_keys(value)
                return cls
            setattr(cls, 'set_' + arg, setter)
        return cls
    return inner

def clickable(*args):
    def inner(cls):
        for arg in args:
            def clicker(cls):
                cls.click_on(arg)
                return cls
            setattr(cls, 'click_on_' + arg, clicker)
        return cls
    return inner
