import Oasys.gRPC


# Metaclass for static properties and constants
class DatumType(type):
    _consts = {'CONSTANT_X', 'CONSTANT_Y', 'CONSTANT_Y2', 'FILL_ABOVE_BELOW', 'FILL_RIGHT_LEFT', 'LABEL_10_POINT', 'LABEL_12_POINT', 'LABEL_14_POINT', 'LABEL_18_POINT', 'LABEL_24_POINT', 'LABEL_8_POINT', 'LABEL_ABOVE_CENTRE', 'LABEL_ABOVE_LEFT', 'LABEL_ABOVE_RIGHT', 'LABEL_AUTOMATIC', 'LABEL_BELOW_CENTRE', 'LABEL_BELOW_LEFT', 'LABEL_BELOW_RIGHT', 'LABEL_BOTTOM_LEFT', 'LABEL_BOTTOM_RIGHT', 'LABEL_COURIER_BOLD', 'LABEL_COURIER_MEDIUM', 'LABEL_DEFAULT', 'LABEL_HELVETICA_BOLD', 'LABEL_HELVETICA_MEDIUM', 'LABEL_HORIZONTAL', 'LABEL_MIDDLE_LEFT', 'LABEL_MIDDLE_RIGHT', 'LABEL_NONE', 'LABEL_TIMES_BOLD', 'LABEL_TIMES_MEDIUM', 'LABEL_TOP_LEFT', 'LABEL_TOP_RIGHT', 'LABEL_VERTICAL', 'POINTS'}

    def __getattr__(cls, name):
        if name in DatumType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Datum(Oasys.gRPC.OasysItem, metaclass=DatumType):
    _props = {'acronym', 'fill_colour_above', 'fill_colour_below', 'fill_colour_between', 'fill_colour_left', 'fill_colour_right', 'fill_type', 'label', 'label2', 'label_colour', 'label_font', 'label_orientation', 'label_position', 'label_size', 'line_colour', 'line_style', 'line_width'}


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Datum._props:
            return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Datum._props:
            Oasys.THIS._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, acronym, type, value, second_value=Oasys.gRPC.defaultArg):
        handle = Oasys.THIS._connection.constructor(self.__class__.__name__, acronym, type, value, second_value)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# Static methods
    def Delete(datum):
        """
        Deletes a datum

        Parameters
        ----------
        datum : string
            Acronym of datum to delete

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Delete", datum)

    def Exists(datum):
        """
        Checks if a datum exists

        Parameters
        ----------
        datum : string
            Acronym of datum to check

        Returns
        -------
        bool
            True if the datum exists, otherwise False
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Exists", datum)

    def First():
        """
        Returns the first datum

        Returns
        -------
        Datum
            Datum object (or None if there are no datum in the model)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "First")

    def GetFromAcronym(datum):
        """
        Returns the datum object for a datum acronym

        Parameters
        ----------
        datum : string
            Acronym of datum to return object for

        Returns
        -------
        Datum
            Datum object (or None if the datum does not exist)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "GetFromAcronym", datum)



# Instance methods
    def AddToGraph(self, *graph):
        """
        Adds a datum to a graph

        Parameters
        ----------
        *graph : int
            Graph to add the datum to. If undefined then the datum is added to all graphs
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddToGraph", graph)

    def IsOnGraph(self, graph):
        """
        Returns whether a datum is on a graph

        Parameters
        ----------
        graph : int
            Graph id

        Returns
        -------
        bool
            True if it is on the graph, False otherwise
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "IsOnGraph", graph)

    def Next(self):
        """
        Returns the next datum in the model

        Returns
        -------
        Datum
            Datum object (or None if there are no more datums in the model)
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def RemoveFromGraph(self, *graph):
        """
        Removes a datum from a graph

        Parameters
        ----------
        *graph : int
            Graph to remove the datum from. If undefined then the datum is removed from all graphs
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveFromGraph", graph)

