import Oasys.gRPC


# Metaclass for static properties and constants
class VariableType(type):
    _consts = {'DESCRIPTION', 'FORMAT', 'FORMAT_FLOAT', 'FORMAT_GENERAL', 'FORMAT_INTEGER', 'FORMAT_LOWERCASE', 'FORMAT_NONE', 'FORMAT_SCIENTIFIC', 'FORMAT_UPPERCASE', 'NAME', 'PRECISION', 'READONLY', 'TEMPORARY', 'TYPE', 'VALUE'}

    def __getattr__(cls, name):
        if name in VariableType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Variable(Oasys.gRPC.OasysItem, metaclass=VariableType):
    _props = {'description', 'format', 'name', 'precision', 'readonly', 'temporary', 'type', 'value'}


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Variable._props:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Variable._props:
            Oasys.REPORTER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, template, name, description=Oasys.gRPC.defaultArg, value=Oasys.gRPC.defaultArg, type=Oasys.gRPC.defaultArg, readonly=Oasys.gRPC.defaultArg, temporary=Oasys.gRPC.defaultArg):
        handle = Oasys.REPORTER._connection.constructor(self.__class__.__name__, template, name, description, value, type, readonly, temporary)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# Static methods
    def GetAll(template):
        """
        Returns an array of Variable objects for all of the variables in a Template

        Parameters
        ----------
        template : Template
            Template to get the variables from

        Returns
        -------
        list
            List of Variable objects
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetAll", template)

    def GetFromName(template, name):
        """
        Returns the Variable object for a variable name

        Parameters
        ----------
        template : Template
            Template to find the variable in
        name : string
            name of the variable you want the Variable object for

        Returns
        -------
        Variable
            Variable object (or None if variable does not exist)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFromName", template, name)



# Instance methods
    def Remove(self):
        """
        Remove a variable
        Note that if you call this function for a Variable object,
        the Variable data will be deleted, so you should not try to use it afterwards!

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Remove")

