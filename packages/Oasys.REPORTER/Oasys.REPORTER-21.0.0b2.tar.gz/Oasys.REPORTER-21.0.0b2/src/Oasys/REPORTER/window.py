import Oasys.gRPC


# Metaclass for static properties and constants
class WindowType(type):
    _consts = {'CANCEL', 'NO', 'OK', 'YES'}

    def __getattr__(cls, name):
        if name in WindowType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Window(Oasys.gRPC.OasysItem, metaclass=WindowType):


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Error(title, error, buttons=Oasys.gRPC.defaultArg):
        """
        Show an error message in a window

        Parameters
        ----------
        title : string
            Title for window
        error : string
            Error message to show in window
        buttons : constant
            The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        ?
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Error", title, error, buttons)

    def GetDirectory(initial=Oasys.gRPC.defaultArg):
        """
        Map the directory selector box native to your machine, allowing you to choose a directory

        Parameters
        ----------
        initial : string
            Initial directory to start from

        Returns
        -------
        str
            directory (string), (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetDirectory", initial)

    def GetFile(extension=Oasys.gRPC.defaultArg, allow_new=Oasys.gRPC.defaultArg, initial=Oasys.gRPC.defaultArg):
        """
        Map a file selector box allowing you to choose a file.
        See also Window.GetFiles()

        Parameters
        ----------
        extension : string
            Extension to filter by
        allow_new : boolean
            Allow creation of new file
        initial : string
            Initial directory to start from

        Returns
        -------
        str
            filename (string), (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFile", extension, allow_new, initial)

    def GetFiles(extension=Oasys.gRPC.defaultArg):
        """
        Map a file selector box allowing you to choose multiple files.
        See also Window.GetFile()

        Parameters
        ----------
        extension : string
            Extension to filter by

        Returns
        -------
        list
            List of filenames (strings), or None if cancel pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFiles", extension)

    def GetInteger(title, message):
        """
        Map a window allowing you to input an integer. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        int
            Integer. Value input, (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetInteger", title, message)

    def GetNumber(title, message):
        """
        Map a window allowing you to input a number. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        ?
            Real. Value input, (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetNumber", title, message)

    def GetOptions(title, message, options):
        """
        Map a window allowing you to input various options. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        options : list of dicts
            Array of objects listing options that can be set. If OK is pressed the objects will be updated with the values from the widgets. If cancel is pressed they will not

        Returns
        -------
        bool
            False if cancel pressed, True if OK pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetOptions", title, message, options)

    def GetString(title, message):
        """
        Map a window allowing you to input a string. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        ?
            String. Value input, (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetString", title, message)

    def Information(title, info, buttons=Oasys.gRPC.defaultArg):
        """
        Show information in a window

        Parameters
        ----------
        title : string
            Title for window
        info : string
            Information to show in window
        buttons : constant
            The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        ?
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Information", title, info, buttons)

    def Message(title, message, buttons=Oasys.gRPC.defaultArg):
        """
        Show a message in a window

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        buttons : constant
            The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        ?
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Message", title, message, buttons)

    def Question(title, question, buttons=Oasys.gRPC.defaultArg):
        """
        Show a question in a window

        Parameters
        ----------
        title : string
            Title for window
        question : string
            Question to show in window
        buttons : constant
            The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted Yes and No button will be used

        Returns
        -------
        ?
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Question", title, question, buttons)

    def Warning(title, warning, buttons=Oasys.gRPC.defaultArg):
        """
        Show a warning message in a window

        Parameters
        ----------
        title : string
            Title for window
        warning : string
            Warning message to show in window
        buttons : constant
            The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        ?
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Warning", title, warning, buttons)

