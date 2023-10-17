import Oasys.gRPC


# Metaclass for static properties and constants
class SymbolType(type):
    _consts = {'CIRCLE', 'CROSS', 'DIAMOND', 'DOT', 'HOURGLASS', 'NONE', 'SQUARE', 'STAR', 'TRIANGLE'}

    def __getattr__(cls, name):
        if name in SymbolType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Symbol(Oasys.gRPC.OasysItem, metaclass=SymbolType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
