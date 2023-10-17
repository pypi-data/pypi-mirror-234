import Oasys.gRPC


# Metaclass for static properties and constants
class IncludeType(type):
    _consts = {'NATIVE', 'UNIX', 'WINDOWS'}

    def __getattr__(cls, name):
        if name in IncludeType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Include(Oasys.gRPC.OasysItem, metaclass=IncludeType):


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
