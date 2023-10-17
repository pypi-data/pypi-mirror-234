import Oasys.gRPC


# Metaclass for static properties and constants
class LineStyleType(type):
    _consts = {'DASH', 'DASH2', 'DASH3', 'DASH4', 'DASH5', 'DASH6', 'NONE', 'SOLID'}

    def __getattr__(cls, name):
        if name in LineStyleType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class LineStyle(Oasys.gRPC.OasysItem, metaclass=LineStyleType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
