class ObjectMappingNotFound(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

class InvalidObjectMapping(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)