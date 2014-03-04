class Finder:

    def __init__(self, root_node):
        self._root_node = root_node

    def by_xpath(self, expression, *args, **kwargs):
        return ExpressionBuilder(self, 'by_xpath', expression, *args, **kwargs)

    def by_css(self, expression, *args, **kwargs):
        return ExpressionBuilder(self, 'by_css', expression, *args, **kwargs)

    def by_id(self, expression, *args, **kwargs):
        return ExpressionBuilder(self, 'by_id', expression, *args, **kwargs)

    @property
    def root_node(self):
        return self._root_node


class ExpressionBuilder:

    _detection_type = {
        'by_xpath': 'find_elements_by_xpath',
        'by_css': 'find_elements_by_css_selector',
        'by_id': 'find_elements_by_id'
    }

    def __init__(self, finder, method_name, expression, *args, **kwargs):
        self._finder = finder
        self._method_name = method_name
        self._expression = expression
        self._args = args
        self._kwargs = kwargs

    def build(self):
        ftype = self._detection_type[self._method_name]
        return lambda: getattr(self._finder.root_node, ftype)(self._expression.format(self._args, self._kwargs))
