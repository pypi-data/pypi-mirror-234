import Oasys.gRPC


# Metaclass for static properties and constants
class PageType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Page(Oasys.gRPC.OasysItem, metaclass=PageType):


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
    def AddGraph(page_number, graph_number=Oasys.gRPC.defaultArg, graph_number_to_copy_properties_from=Oasys.gRPC.defaultArg, number_of_graphs=Oasys.gRPC.defaultArg):
        """
        Adds one or more graphs to the specified page

        Parameters
        ----------
        page_number : Integer
            Page number to add graph(s) to
        graph_number : Integer
            Graph number to add to page. If this argument is 0 or not given, a new graph is created
        graph_number_to_copy_properties_from : Integer
            If the second argument is 0, this specifies which graph to copy properties from when creating new graphs
        number_of_graphs : Integer
            If the second argument is 0, this specifies the number of new graphs to create and add to the specified page

        Returns
        -------
        bool
            True if the graph was added, False if failed
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "AddGraph", page_number, graph_number, graph_number_to_copy_properties_from, number_of_graphs)

    def Layout(page_number, layout, num_in_x=Oasys.gRPC.defaultArg, num_in_y=Oasys.gRPC.defaultArg):
        """
        Sets the layout of either all pages or a specified page

        Parameters
        ----------
        page_number : Integer
            Page number for which to set layout. If this argument is 0 then layout will be set on all pages individually. If -1 then the layout will be set globally, as in the 'Graphs' panel
        layout : String or Integer
            Layout specifier. Options are: "wide" or 1 - Tile wide, "tall" or 2 - Tile tall, "1x1" or 3 - 1x1, "2x2" or 4 - 2x2, "3x3" or 5 - 3x3, "xy" or 6 - XxY
        num_in_x : Integer
            Number of graphs in X-direction if user-defined XxY layout (6)
        num_in_y : Integer
            Number of graphs in Y-direction if user-defined XxY layout (6)

        Returns
        -------
        bool
            True if the layout was set, False if failed
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Layout", page_number, layout, num_in_x, num_in_y)

    def RemoveGraph(page_number, graph_number=Oasys.gRPC.defaultArg, lower_end_of_range_for_removing_graphs=Oasys.gRPC.defaultArg, upper_end_of_range_for_removing_graphs=Oasys.gRPC.defaultArg):
        """
        Remove one or more graphs from the specified page

        Parameters
        ----------
        page_number : Integer
            Page number to remove the graph from
        graph_number : Integer
            Graph number to remove from page. If this argument is 0 or not given, the highest number graph on the page will be removed. If this argument is -1, all graphs will be removed
        lower_end_of_range_for_removing_graphs : Integer
            If the second argument is 0, this specifies the lower end of the range for removing graphs. All graphs with numbers within the specified range will be removed from the page
        upper_end_of_range_for_removing_graphs : Integer
            If the second argument is 0, this specifies the upper end of the range for removing graphs. All graphs with numbers within the specified range will be removed from the page. If this argument is not given then it will be set to 32 by default

        Returns
        -------
        bool
            True if the graph was removed, False if failed
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "RemoveGraph", page_number, graph_number, lower_end_of_range_for_removing_graphs, upper_end_of_range_for_removing_graphs)

    def ReturnActivePage():
        """
        Returns the current active page in T/HIS

        Returns
        -------
        int
            integer
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "ReturnActivePage")

    def ReturnGraphs(page_number):
        """
        Returns the graphs on the specified page as an array of Graph objects

        Parameters
        ----------
        page_number : Integer
            Page number for which to return the graphs it contains

        Returns
        -------
        list
            List of Graph objects
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "ReturnGraphs", page_number)

    def SetActivePage(page_number):
        """
        Sets the current active page in T/HIS, returning -1 if the page does not exist or the page number if it does

        Parameters
        ----------
        page_number : Integer
            Page number to set to active page

        Returns
        -------
        bool
            True if the page was set, False if the page does not exist
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "SetActivePage", page_number)

