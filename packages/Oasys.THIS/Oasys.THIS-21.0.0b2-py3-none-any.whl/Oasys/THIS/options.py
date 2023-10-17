import Oasys.gRPC


# Metaclass for static properties and constants
class OptionsType(type):
    _consts = {'RUN_PROMISE_CONSTRUCTOR', 'RUN_PROMISE_METHOD', 'RUN_PROMISE_PROPERTY', 'RUN_PROMISE_WINDOW_LOOP'}
    _props = {'auto_confirm', 'max_widgets', 'max_window_lines', 'run_promises', 'ssh_buffer_size'}

    def __getattr__(cls, name):
        if name in OptionsType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)
        if name in OptionsType._props:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Options(Oasys.gRPC.OasysItem, metaclass=OptionsType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
