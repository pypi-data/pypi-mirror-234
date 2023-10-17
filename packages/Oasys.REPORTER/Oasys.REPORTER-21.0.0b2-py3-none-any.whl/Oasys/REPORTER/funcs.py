import Oasys.gRPC


def Batch():
    """
    This method can be used to test whether REPORTER is running in batch mode or not

    Returns
    -------
    ?
        True/False
    """
    return Oasys.REPORTER._connection.functionCall("Batch")


def Debug(string):
    """
    Print a string to log file for debugging. Anything that you call the debug method on will
    be 'printed' to the log file window. Note that a carriage return will automatically be added

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to debug

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("Debug", string)


def Exit():
    """
    Stop execution and exit from script

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("Exit")


def GetCurrentDirectory():
    """
    Return the current working directory for REPORTER

    Returns
    -------
    ?
        string
    """
    return Oasys.REPORTER._connection.functionCall("GetCurrentDirectory")


def LogError(message):
    """
    Print an error to log file. Anything that you print will be output
    to the log file window in bold red text. Note that a carriage return will automatically be added

    Parameters
    ----------
    message : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("LogError", message)


def LogPrint(message):
    """
    Print a string to log file. Anything that you print will be output
    to the log file window. Note that a carriage return will automatically be added

    Parameters
    ----------
    message : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("LogPrint", message)


def LogWarning(message):
    """
    Print a warning to log file. Anything that you print will be output
    to the log file window in red text. Note that a carriage return will automatically be added

    Parameters
    ----------
    message : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("LogWarning", message)


def Output(string):
    """
    Output a string from a script. Note that a carriage return is not automatically added

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("Output", string)


def SetCurrentDirectory(directory):
    """
    Set the current working directory for REPORTER

    Parameters
    ----------
    directory : string
        The directory that you want to change to

    Returns
    -------
    bool
        True if successful, False if not
    """
    return Oasys.REPORTER._connection.functionCall("SetCurrentDirectory", directory)


def System(string):
    """
    Do a system command outside REPORTER

    Parameters
    ----------
    string : Any valid javascript type
        The system command that you want to do

    Returns
    -------
    int
        integer (probably zero if command successful but is implementation-dependant)
    """
    return Oasys.REPORTER._connection.functionCall("System", string)
