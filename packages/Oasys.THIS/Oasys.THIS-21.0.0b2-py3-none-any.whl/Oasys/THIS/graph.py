import Oasys.gRPC


# Metaclass for static properties and constants
class GraphType(type):
    _consts = {'AXIS_LINEAR', 'AXIS_LOG', 'FONT_COURIER_BOLD', 'FONT_COURIER_MEDIUM', 'FONT_DEFAULT', 'FONT_HELVETICA_BOLD', 'FONT_HELVETICA_MEDIUM', 'FONT_SIZE_10', 'FONT_SIZE_12', 'FONT_SIZE_14', 'FONT_SIZE_18', 'FONT_SIZE_24', 'FONT_SIZE_8', 'FONT_SIZE_AUTO', 'FONT_TIMES_BOLD', 'FONT_TIMES_MEDIUM', 'GRID_OFF', 'GRID_ON', 'LEGEND_1_COLUMN', 'LEGEND_2_COLUMN', 'LEGEND_AUTO', 'LEGEND_COLUMN_LIST', 'LEGEND_FLOATING', 'LEGEND_OFF', 'NO', 'OFF', 'ON', 'PREFIX_AUTO', 'PREFIX_DIR', 'PREFIX_MODEL_NUMBER', 'PREFIX_OFF', 'PREFIX_ON', 'PREFIX_THF', 'PREFIX_USER_DEFINED', 'YES'}

    def __getattr__(cls, name):
        if name in GraphType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Graph(Oasys.gRPC.OasysItem, metaclass=GraphType):
    _props = {'active', 'add_x_units', 'add_y2_units', 'add_y_units', 'auto_title', 'auto_xlabel', 'auto_xmax', 'auto_xmin', 'auto_y2label', 'auto_y2max', 'auto_y2min', 'auto_ylabel', 'auto_ymax', 'auto_ymin', 'background_colour', 'foreground_colour', 'grid', 'id', 'legend_background_colour', 'legend_background_trans', 'legend_font', 'legend_font_colour', 'legend_font_size', 'legend_layout', 'legend_prefix_format', 'legend_show_prefix', 'legend_show_user_lines', 'legend_user_line_1', 'legend_user_line_1_size', 'legend_user_line_2', 'legend_user_line_2_size', 'legend_user_line_3', 'legend_user_line_3_size', 'legend_user_line_4', 'legend_user_line_4_size', 'legend_user_line_5', 'legend_user_line_5_size', 'legend_user_line_6', 'legend_user_line_6_size', 'legend_user_lines_colour', 'legend_user_lines_font', 'num_legend_columns', 'show_title', 'show_xlabel', 'show_y2label', 'show_ylabel', 'title', 'x_axis_type', 'x_unit_colour', 'x_unit_decimals', 'x_unit_font', 'x_unit_format', 'x_unit_size', 'xlabel', 'xlabel_colour', 'xlabel_font', 'xlabel_size', 'xmax', 'xmin', 'y2_axis_type', 'y2_unit_colour', 'y2_unit_decimals', 'y2_unit_font', 'y2_unit_format', 'y2_unit_size', 'y2label', 'y2label_colour', 'y2label_font', 'y2label_size', 'y2max', 'y2min', 'y_axis_type', 'y_unit_colour', 'y_unit_decimals', 'y_unit_font', 'y_unit_format', 'y_unit_size', 'ylabel', 'ylabel_colour', 'ylabel_font', 'ylabel_size', 'ymax', 'ymin'}


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Graph._props:
            return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Graph._props:
            Oasys.THIS._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, index=Oasys.gRPC.defaultArg):
        handle = Oasys.THIS._connection.constructor(self.__class__.__name__, index)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# Static methods
    def DeleteFromID(id):
        """
        Deletes a graph

        Parameters
        ----------
        id : integer
            ID of graph to delete

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "DeleteFromID", id)

    def GetFromID(id):
        """
        Returns the graph object for a given graph id

        Parameters
        ----------
        id : integer
            ID of graph to return the graph for

        Returns
        -------
        Graph
            Graph object or None if graph does not exists
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "GetFromID", id)

    def Total():
        """
        Returns the total number of graphs

        Returns
        -------
        int
            integer
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def AddCurveID(self, curve_id, no_redraw=Oasys.gRPC.defaultArg):
        """
        Adds a curve to the graph

        Parameters
        ----------
        curve_id : Integer
            ID of the curve to add
        no_redraw : Integer
            If this argument is 1 then the graph will not be redrawn after the curve is added. This is to be used if a large number of curves are to be added to a graph, so as to avoid the same curves being drawn multiple times. No argument or 0 will trigger a redraw after the curve is added

        Returns
        -------
        bool
            Returns True if the curve is successfully added to the graph else it would return False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddCurveID", curve_id, no_redraw)

    def AddToPage(self, page_number):
        """
        Adds the graph to the page

        Parameters
        ----------
        page_number : Integer
            Page number for which to add the graph to

        Returns
        -------
        bool
            Returns True if the graph is successfully added to the page else it would return False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddToPage", page_number)

    def Delete(self):
        """
        Deletes the graph

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def GetAllCurveIDs(self):
        """
        Returns the IDs of the curves present in the graph in an array

        Returns
        -------
        list
            List integers
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAllCurveIDs")

    def GetAllPageIDs(self):
        """
        Returns all the pages containing the graph

        Returns
        -------
        list
            List of integers
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAllPageIDs")

    def GetNumCurves(self):
        """
        Returns number curves present in the graph

        Returns
        -------
        int
            Number of curves present in the graph
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNumCurves")

    def Lock(self, lock_type):
        """
        Locks the blanking status of either blanked curves, unblanked curves or all curves on the graph

        Parameters
        ----------
        lock_type : Integer
            No argument or 0 to lock blanked curves, -1 to unlock blanked curves, -2 to unfreeze all visible curves

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Lock", lock_type)

    def RemoveCurveID(self, id):
        """
        Removes a curve from the graph

        Parameters
        ----------
        id : Integer
            ID of the curve to be removed

        Returns
        -------
        bool
            Returns True if the curve is successfully removed from the graph else it would return False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveCurveID", id)

    def RemoveFromPage(self, id):
        """
        Removes the graph from a page

        Parameters
        ----------
        id : Integer
            ID of the page from which the graph is to be removed

        Returns
        -------
        bool
            Returns True if the graph is successfully removed from the page else it would return False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveFromPage", id)

