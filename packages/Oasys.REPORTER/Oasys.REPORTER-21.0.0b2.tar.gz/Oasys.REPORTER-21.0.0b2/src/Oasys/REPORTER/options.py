import Oasys.gRPC


# Metaclass for static properties and constants
class OptionsType(type):
    _consts = {'RUN_PROMISE_CONSTRUCTOR', 'RUN_PROMISE_METHOD', 'RUN_PROMISE_PROPERTY', 'RUN_PROMISE_SCRIPT', 'RUN_PROMISE_WINDOW_LOOP'}
    _props = {'run_promises'}

    def __getattr__(cls, name):
        if name in OptionsType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)
        if name in OptionsType._props:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Options(Oasys.gRPC.OasysItem, metaclass=OptionsType):


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
