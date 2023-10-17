import Oasys.gRPC

# ItemObject not (yet) used in T/HIS but defined here for consistency with PRIMER

class ItemObject(Oasys.gRPC.OasysItem):

    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)


    def __setattr__(self, name, value):
        Oasys.THIS._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
        return
