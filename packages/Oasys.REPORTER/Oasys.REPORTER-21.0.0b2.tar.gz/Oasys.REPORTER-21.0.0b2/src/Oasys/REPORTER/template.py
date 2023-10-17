import Oasys.gRPC


# Metaclass for static properties and constants
class TemplateType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Template(Oasys.gRPC.OasysItem, metaclass=TemplateType):
    _props = {'view'}
    _rprops = {'filename', 'pages', 'path'}


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Template._props:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Template._rprops:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Template._props:
            Oasys.REPORTER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Template._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, filename=Oasys.gRPC.defaultArg):
        handle = Oasys.REPORTER._connection.constructor(self.__class__.__name__, filename)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# Static methods
    def GetAll():
        """
        Get all of the open templates

        Returns
        -------
        list
            List of Template objects or None if no open templates
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetAll")

    def GetCurrent():
        """
        Get the currently active template

        Returns
        -------
        Template
            Template object or None if no active template
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetCurrent")



# Instance methods
    def Close(self):
        """
        Close a template.
        Note that if you call this function for a Template object,
        the Template data will be deleted, so you should not try to use it afterwards!

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Close")

    def DeletePage(self, index):
        """
        Deletes a page from a template

        Parameters
        ----------
        index : integer
            The index of the page that you want to delete. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeletePage", index)

    def DeleteTemporaryVariables(self):
        """
        Deletes any temporary variables from a template

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeleteTemporaryVariables")

    def EditVariables(self, title=Oasys.gRPC.defaultArg, message=Oasys.gRPC.defaultArg, update=Oasys.gRPC.defaultArg, variables=Oasys.gRPC.defaultArg, columns=Oasys.gRPC.defaultArg, alphabetical=Oasys.gRPC.defaultArg):
        """
        Start a dialog to edit the template variables

        Parameters
        ----------
        title : string
            Title for dialog. If omitted, null or an empty string is given then the default title will be used
        message : string
            Message to show in dialog. If omitted, null or an empty string is given then the default message will be used
        update : boolean
            Whether the variables in the template will be updated with the new values if OK is pressed.
            Setting this to be false allows you to check variable values before updating them from a script.
            If omitted the default is true
        variables : array
            A list of variables to show in the dialog.
            If omitted, null or an empty array, all variables will be shown
        columns : constant
            Columns to show in the dialog (as well as the variable value column).
            Can be a bitwise OR of Variable.NAME,
            Variable.TYPE,
            Variable.DESCRIPTION,
            Variable.FORMAT,
            Variable.PRECISION and
            Variable.TEMPORARY.
            If omitted columns will be shown for name and description
        alphabetical : boolean
            Whether to sort variables in the table by alphabetical order.
            If false, variables are listed in the order they are passed in the optional variables argument.
            If no variables are passed to the function, all template variables will be shown in alphabetical order.
            If omitted, the default value is true

        Returns
        -------
        dict
            Dict containing the variable names and values or None if cancel was pressed
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "EditVariables", title, message, update, variables, columns, alphabetical)

    def ExpandVariablesInString(self, string):
        """
        Replaces any variables in a string with their current values

        Parameters
        ----------
        string : string
            The string you want to expand variables in

        Returns
        -------
        str
            String (string) with variables expanded. If a variable in a string does not exist it is replaced by a blank
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExpandVariablesInString", string)

    def Generate(self):
        """
        Generate a template

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Generate")

    def GetAllPages(self):
        """
        Gets all of the pages from a template

        Returns
        -------
        list
            List of Page objects
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAllPages")

    def GetMaster(self):
        """
        Get the master page from a template

        Returns
        -------
        Page
            Page object
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetMaster")

    def GetPage(self, index):
        """
        Get a page from a template

        Parameters
        ----------
        index : integer
            The index of the page that you want to get. Note that indices start at 0

        Returns
        -------
        Page
            Page object
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPage", index)

    def GetVariableDescription(self, name):
        """
        Get the description for a variable

        Parameters
        ----------
        name : string
            Variable name you want to get description for

        Returns
        -------
        str
            Variable description (string) or None if variable does not exist
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetVariableDescription", name)

    def GetVariableValue(self, name):
        """
        Get the value for a variable

        Parameters
        ----------
        name : string
            Variable name you want to get value for

        Returns
        -------
        str
            Variable value (string) or None if variable does not exist
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetVariableValue", name)

    def Html(self, filename):
        """
        Save a template as HTML

        Parameters
        ----------
        filename : string
            Filename you want to save

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Html", filename)

    def Pdf(self, filename):
        """
        Save a template as Adobe Acrobat PDF

        Parameters
        ----------
        filename : string
            Filename you want to save

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Pdf", filename)

    def Pptx(self, filename):
        """
        Save a template as PowerPoint

        Parameters
        ----------
        filename : string
            Filename you want to save

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Pptx", filename)

    def Print(self, printer):
        """
        Print template on a printer

        Parameters
        ----------
        printer : string
            Printer you want to print to

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Print", printer)

    def Save(self):
        """
        Save a template

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Save")

    def SaveAs(self, filename):
        """
        Save a template/report with a new name

        Parameters
        ----------
        filename : string
            Filename you want to save. Note if you use the .orr extension the template will be saved as a report if generated

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SaveAs", filename)

    def Update(self):
        """
        Update/redraw a template

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Update")

