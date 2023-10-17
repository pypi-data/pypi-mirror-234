import Oasys.gRPC


def AllocateFlag():
    """
    Allocate a flag for use in the script. See also
    ReturnFlag() and
    Once allocated the flag is automatically cleared for all entity types and all the curves currently in T/HIS

    Returns
    -------
    ?
        Flag (integer)
    """
    return Oasys.THIS._connection.functionCall("AllocateFlag")


def ClearFlag(flag):
    """
    Clears a flag on all curves and entity types

    Parameters
    ----------
    flag : Flag
        The flag to return

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("ClearFlag", flag)


def DialogueInput(*command):
    """
    Execute one or more lines of command line dialogue input

    Parameters
    ----------
    *command : string
        Command to execute (as if it had been typed into the dialogue box)
        This argument can be repeated if required.
        Alternatively a single array argument containing the multiple values can be given

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("DialogueInput", command)


def DialogueInputNoEcho(*command):
    """
    Execute one or more lines of command line dialogue input with no echo of commands to dialogue box

    Parameters
    ----------
    *command : string
        Command to execute (as if it had been typed into the dialogue box)
        This argument can be repeated if required.
        Alternatively a single array argument containing the multiple values can be given

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("DialogueInputNoEcho", command)


def DisableGraphWindowUpdates():
    """
    Disable Graph Window updates

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("DisableGraphWindowUpdates")


def DisableMenuUpdates():
    """
    Disable menu system updates

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("DisableMenuUpdates")


def EnableGraphWindowUpdates():
    """
    Enable Graph Window updates

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("EnableGraphWindowUpdates")


def EnableMenuUpdates():
    """
    Enable menu system updates

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("EnableMenuUpdates")


def ErrorMessage(string):
    """
    Print an error message to the dialogue box adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("ErrorMessage", string)


def Execute(data):
    """
    Execute a program or script outside T/HIS and get the standard output and error streams

    Parameters
    ----------
    data : dict
        Execute data

    Returns
    -------
    dict
        Dict with properties
    """
    return Oasys.THIS._connection.functionCall("Execute", data)


def Exit(write_hook_interrupt=Oasys.gRPC.defaultArg):
    """
    Exit script

    Parameters
    ----------
    write_hook_interrupt : boolean
        If Exit() is called from a write_hook.js script, the first argument will be processed as in the following: 
        If the argument is provided and set to "true", it is used to interrupt the write out of the model, so that 
        the script exits without anything being written out. An argument value of "false" exits the script and allows 
        the model to be written out as normal. An example of this function's use in a Write Hook script can be found at 
        $OA_INSTALL/primer_library/scripts/hooks/example_write_hook.js

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("Exit", write_hook_interrupt)


def GetCurrentDirectory():
    """
    Get the current working directory

    Returns
    -------
    str
        String containing current working directory
    """
    return Oasys.THIS._connection.functionCall("GetCurrentDirectory")


def GetFtcfVar(name):
    """
    Get the value of a FAST-TCF variable

    Parameters
    ----------
    name : string
        The FAST-TCF variable name (case independent)

    Returns
    -------
    str
        String containing variable value or None if variable does not exist
    """
    return Oasys.THIS._connection.functionCall("GetFtcfVar", name)


def GetInstallDirectory():
    """
    Get the directory in which executables are installed. This is the OA_INSTALL environment variable,
    or if that is not set the directory in which the current executable is installed. Returns NULL if not found

    Returns
    -------
    ?
        string
    """
    return Oasys.THIS._connection.functionCall("GetInstallDirectory")


def GetPreferenceValue(program, name):
    """
    Get the Preference value with the given string in the any of 
    admin ("OA_ADMIN") or install ("OA_INSTALL") or home ("OA_HOME") directory oa_pref

    Parameters
    ----------
    program : string
        The program name string : Valid values are 'All', 'D3Plot', 'Primer', 'Reporter', 'Shell',
        'T/His'
    name : string
        The preference name string

    Returns
    -------
    ?
        : String containing preference value or None if preference string is not present in any oa_pref.
        Also if none of the above environment variables are not present, then API simply returns null.
        While returning preference value, locked preference value in admin and then install oa_pref takes precedence over home oa_pref.
        	If preference is not locked in any of these oa_pref, preference in home directory oa_pref is returned
    """
    return Oasys.THIS._connection.functionCall("GetPreferenceValue", program, name)


def GetStartInDirectory():
    """
    Get the directory passed to T/HIS by the -start_in command line argument

    Returns
    -------
    str
        String containing start_in directory or None if not set
    """
    return Oasys.THIS._connection.functionCall("GetStartInDirectory")


def Getenv(name):
    """
    Get the value of an environment variable

    Parameters
    ----------
    name : string
        The environment variable name

    Returns
    -------
    str
        String containing variable value or None if variable does not exist
    """
    return Oasys.THIS._connection.functionCall("Getenv", name)


def Message(string):
    """
    Print a message to the dialogue box adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print. If '\r' is added to the end of the string then
        instead of automatically adding a carriage return in the dialogue box, the next message will overwrite 
        the current one. This may be useful for giving feedback to the dialogue box when doing an operation

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("Message", string)


def MilliSleep(time):
    """
    Pause execution of the script for time milliseconds. See also
    Sleep()

    Parameters
    ----------
    time : integer
        Number of milliseconds to pause for

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("MilliSleep", time)


def NumberToString(number, width, pref_int=Oasys.gRPC.defaultArg):
    """
    Formats a number to a string with the specified width

    Parameters
    ----------
    number : integer/float
        The number you want to format
    width : integer
        The width of the string you want to format it to (must be less than 80)
    pref_int : boolean
        By default only integer values inside the single precision 32 bit signed integer limit of approximately
        +/-2e9 are formatted as integers, all other numeric values are formatted as floats. With this argument set to TRUE then
        integer values up to the mantissa precision of a 64 bit float, approximately +/-9e15, will also be formatted as integers

    Returns
    -------
    str
        String containing the number
    """
    return Oasys.THIS._connection.functionCall("NumberToString", number, width, pref_int)


def OpenManual(program, page):
    """
    Open the Oasys manuals at a requested page

    Parameters
    ----------
    program : string
        The program manual to open. Can be "primer", "d3plot" or "this"
    page : string
        The page to open in the manual, e.g. "running-this.html"

    Returns
    -------
    bool
        True if successful, False if not
    """
    return Oasys.THIS._connection.functionCall("OpenManual", program, page)


def Plot():
    """
    Updates all the T/HIS graphs

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("Plot")


def Print(string):
    """
    Print a string to stdout. Note that a carriage return is not added

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("Print", string)


def Println(string):
    """
    Print a string to stdout adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("Println", string)


def ReturnFlag(flag):
    """
    Return a flag used in the script. See also
    AllocateFlag() and

    Parameters
    ----------
    flag : Flag
        The flag to return

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("ReturnFlag", flag)


def SetCurrentDirectory(directory_path):
    """
    Sets the current working directory

    Parameters
    ----------
    directory_path : string
        Path to the directory you would like to change into

    Returns
    -------
    bool
        True if successful, False if not
    """
    return Oasys.THIS._connection.functionCall("SetCurrentDirectory", directory_path)


def SetFtcfVar(name):
    """
    Set the value of a FAST-TCF variable. If the variable already exists then it's value is updated

    Parameters
    ----------
    name : string
        The FAST-TCF variable name (case independent)

    Returns
    -------
    str
        String containing variable value or None if variable does not exist
    """
    return Oasys.THIS._connection.functionCall("SetFtcfVar", name)


def Sleep(time):
    """
    Pause execution of the script for time seconds. See also
    MilliSleep()

    Parameters
    ----------
    time : integer
        Number of seconds to pause for

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("Sleep", time)


def System(string):
    """
    Do a system command outside T/HIS. To run an external command and get the output then please use
    Execute() instead

    Parameters
    ----------
    string : Any valid javascript type
        The system command that you want to do

    Returns
    -------
    int
        integer (probably zero if command successful but is implementation-dependant)
    """
    return Oasys.THIS._connection.functionCall("System", string)


def Unix():
    """
    Test whether script is running on a Unix/Linux operating system. See also
    Windows()

    Returns
    -------
    bool
        True if Unix/Linux, False if not
    """
    return Oasys.THIS._connection.functionCall("Unix")


def UpdateCurveMenu():
    """
    Updates the scroll bar in the Curve Manager. Useful if your script has created lots of new curves and you want to update the menu (otherwise, the scroll bar range will only be updated when the script exits)

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("UpdateCurveMenu")


def WarningMessage(string):
    """
    Print a warning message to the dialogue box adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.THIS._connection.functionCall("WarningMessage", string)


def Windows():
    """
    Test whether script is running on a Windows operating system. See also
    Unix()

    Returns
    -------
    bool
        True if Windows, False if not
    """
    return Oasys.THIS._connection.functionCall("Windows")
