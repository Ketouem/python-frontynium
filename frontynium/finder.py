class Finder:

    def __init__(self, root_node):
        self._root_node = root_node

    def by_xpath(self, expression, single_element=True, *args, **kwargs):
        return ExpressionBuilder(self, 'by_xpath', expression, single_element, *args, **kwargs)

    def by_css(self, expression, single_element=True, *args, **kwargs):
        return ExpressionBuilder(self, 'by_css', expression, single_element, *args, **kwargs)

    def by_id(self, expression, single_element=True, *args, **kwargs):
        return ExpressionBuilder(self, 'by_id', expression, single_element, *args, **kwargs)

    @property
    def root_node(self):
        return self._root_node


class ExpressionBuilder:

    _detection_type = {
        'by_xpath': lambda s: 'find_element{0}_by_xpath'.format('s' if not s else ''),
        'by_css': lambda s: 'find_element{0}_by_css_selector'.format('s' if not s else ''),
        'by_id': lambda s: 'find_element{0}_by_id'.format('s' if not s else '')
    }

    def __init__(self, finder, method_name, expression, single_element, *args, **kwargs):
        self._finder = finder
        self._method_name = method_name
        self._expression = expression
        self._single_element = single_element
        self._args = args
        self._kwargs = kwargs

    def build(self):
        ftype = self._detection_type[self._method_name](self._single_element)
        return lambda: getattr(self._finder.root_node, ftype)(self._expression.format(self._args, self._kwargs))