class Page(object):

    _objects = {}

    def __init__(self, webdriver):
        """Default constructor

        webdriver -- instance of selenium's webdriver
        """
        self._webdriver = webdriver

    #Preventing a var = Page(webdriver) in a test code as _objects needs to be defined correctly
    def __new__(cls, *args, **kwargs):
        if cls is Page:
            raise TypeError("This class is not meant to be instantiated directly but subclassed")
        return object.__new__(cls, *args, **kwargs)

    @property
    def webdriver(self):
        return self._webdriver

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, value):
        self._objects = value