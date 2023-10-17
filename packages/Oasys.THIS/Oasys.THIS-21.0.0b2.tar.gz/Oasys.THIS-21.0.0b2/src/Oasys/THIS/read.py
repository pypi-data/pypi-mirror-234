import Oasys.gRPC


# Metaclass for static properties and constants
class ReadType(type):
    _consts = {'CSV_COMMA', 'CSV_SPACE', 'CSV_TAB', 'CSV_XYXY', 'CSV_XYYY', 'DIADEM_COMMENT', 'DIADEM_NAME', 'EQUATION_CURVE_VARS', 'EQUATION_X_OR_CURVE', 'EQUATION_X_VALS', 'ISO_CHANNEL_CODE', 'ISO_CHANNEL_LABEL', 'ISO_MULTIPLE_CHANNELS', 'ISO_SINGLE_CHANNEL', 'LSPP_CURVE_FILE', 'LSPP_XY_PAIRS'}

    def __getattr__(cls, name):
        if name in ReadType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Read(Oasys.gRPC.OasysItem, metaclass=ReadType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Bulk(filename, options=Oasys.gRPC.defaultArg):
        """
        Reads a Bulk Data file into T/HIS

        Parameters
        ----------
        filename : String
            Name of Bulk Data file to read
        options : dict
            Options which give you greater control of reading a Bulk file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Bulk", filename, options)

    def CSV(filename, options=Oasys.gRPC.defaultArg):
        """
        Reads a CSV file into T/HIS

        Parameters
        ----------
        filename : String
            Name of CSV file to read
        options : dict
            Options which give you greater control of reading a CSV file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "CSV", filename, options)

    def Cur(filename, options=Oasys.gRPC.defaultArg):
        """
        Reads a Curve file into T/HIS

        Parameters
        ----------
        filename : String
            Name of Curve file to read
        options : dict
            Options which give you greater control of reading a Curve file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Cur", filename, options)

    def DIAdem(filename, x_axis_channel, options=Oasys.gRPC.defaultArg):
        """
        Reads a DIAdem file into T/HIS

        Parameters
        ----------
        filename : String
            Name of DIAdem header file to read
        x_axis_channel : integer
            Index of the channel to use as X-axis values. If this is 0 then the X-values can be generated from a start value and an interval in the following two arguments
        options : dict
            Options which give you greater control of reading the Diadem file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "DIAdem", filename, x_axis_channel, options)

    def Equation(formula, options=Oasys.gRPC.defaultArg):
        """
        Create a curve from a user-defined equation

        Parameters
        ----------
        formula : String
            Equation string
        options : dict
            Options which give you greater control of reading the Diadem file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Equation", formula, options)

    def ISO(filename, options=Oasys.gRPC.defaultArg):
        """
        Reads an ISO file into T/HIS

        Parameters
        ----------
        filename : String
            Name of ISO file to read
        options : dict
            Options which give you greater control of reading an ISO file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "ISO", filename, options)

    def Key(filename, options=Oasys.gRPC.defaultArg):
        """
        Reads a Keyword file into T/HIS

        Parameters
        ----------
        filename : String
            Name of Keyword file to read
        options : dict
            Options which give you greater control of reading a Keyword file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Key", filename, options)

    def LSPP(filename, options=Oasys.gRPC.defaultArg):
        """
        Reads an LS-PREPOST file into T/HIS

        Parameters
        ----------
        filename : String
            Name of LS-PREPOST file to read
        options : dict
            Options which give you greater control of reading a Keyword file:

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "LSPP", filename, options)

