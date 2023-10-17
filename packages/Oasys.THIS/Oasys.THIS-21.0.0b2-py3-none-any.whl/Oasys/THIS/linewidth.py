import Oasys.gRPC


# Metaclass for static properties and constants
class LineWidthType(type):
    _consts = {'BOLD', 'FINE', 'HEAVY', 'NORMAL', 'W1', 'W10', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9'}

    def __getattr__(cls, name):
        if name in LineWidthType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class LineWidth(Oasys.gRPC.OasysItem, metaclass=LineWidthType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
