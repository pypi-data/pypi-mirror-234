import Oasys.gRPC


# Metaclass for static properties and constants
class ColourType(type):
    _consts = {'BACKGROUND', 'BLACK', 'BLUE', 'CYAN', 'DARK_GREEN', 'DARK_GREY', 'DARK_MAGENTA', 'FOREGROUND', 'GOLD', 'GREEN', 'HOT_PINK', 'INDIGO', 'LIGHT_GREY', 'LIGHT_PINK', 'LIME', 'MAGENTA', 'MAROON', 'MEDIUM_BLUE', 'MEDIUM_GREEN', 'MEDIUM_GREY', 'NAVY', 'OLIVE', 'ORANGE', 'PALE_YELLOW', 'PINK', 'PURPLE', 'RED', 'SEA_GREEN', 'SKY', 'TURQUOISE', 'USER_1', 'USER_2', 'USER_3', 'USER_4', 'USER_5', 'USER_6', 'USER_n (n = 1 to 150)', 'WHITE', 'YELLOW'}

    def __getattr__(cls, name):
        if name in ColourType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Colour(Oasys.gRPC.OasysItem, metaclass=ColourType):


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
    def GetFromName(name):
        """
        Returns the colour for a given core or user colour name

        Parameters
        ----------
        name : string
            The name of the colour, for example red or user_green or green/cyan

        Returns
        -------
        ?
            colour value (integer)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "GetFromName", name)

    def RGB(red, green, blue):
        """
        Creates a colour from red, green and blue components

        Parameters
        ----------
        red : integer
            red component of colour (0-255)
        green : integer
            green component of colour (0-255)
        blue : integer
            blue component of colour (0-255)

        Returns
        -------
        ?
            colour value (integer)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "RGB", red, green, blue)

