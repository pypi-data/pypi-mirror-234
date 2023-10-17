import Oasys.gRPC


# Metaclass for static properties and constants
class GroupType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Group(Oasys.gRPC.OasysItem, metaclass=GroupType):
    _props = {'crv_at_ymax', 'crv_at_ymin', 'curves', 'name', 'x_at_ymax', 'x_at_ymin', 'x_at_yminpos', 'xmax', 'xmin', 'xminpos', 'ymax', 'ymin', 'yminpos'}


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Group._props:
            return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Group._props:
            Oasys.THIS._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, name):
        handle = Oasys.THIS._connection.constructor(self.__class__.__name__, name)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# Static methods
    def DeleteGroup(group_id_or_name, delete_automatic_groups=Oasys.gRPC.defaultArg):
        """
        Deletes a curve group

        Parameters
        ----------
        group_id_or_name : integer or string
            ID of group to delete or name of group. If this argument is 0, delete all groups. Automatically generated groups won't be deleted unless the next argument is set to 1
        delete_automatic_groups : integer
            If this argument is 1, automatic groups can be deleted. If no argument or 0, automatic groups cant be deleted

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "DeleteGroup", group_id_or_name, delete_automatic_groups)

    def Get(name):
        """
        Returns a group object

        Parameters
        ----------
        name : string
            Name of the group to return object for

        Returns
        -------
        Group
            Group object (or None if the group does not exist)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Get", name)

    def GetFromID(id):
        """
        Returns a group object

        Parameters
        ----------
        id : integer
            ID of the group to return object for

        Returns
        -------
        Group
            Group object (or None if the group does not exist)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "GetFromID", id)

    def Total():
        """
        Returns the total number of curve group currently defined

        Returns
        -------
        int
            Number of curve groups currently defined
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def Add(self, curve):
        """
        Adds a curve object to group

        Parameters
        ----------
        curve : Curve
            Curve that will be added to group

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Add", curve)

    def AddAll(self):
        """
        Adds all curves to group

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddAll")

    def AddID(self, id):
        """
        Adds curve by ID to a group

        Parameters
        ----------
        id : integer
            The ID of the curve you want to add

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddID", id)

    def Contains(self, curve):
        """
        Checks if a curve object is in a curve group

        Parameters
        ----------
        curve : Curve
            Curve that will be checked

        Returns
        -------
        bool
            True if the curve is in the group, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Contains", curve)

    def ContainsID(self, id):
        """
        Checks if a curve ID is in a curve group

        Parameters
        ----------
        id : integer
            The ID of the curve you want to check

        Returns
        -------
        bool
            True if the curve is in the group, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "ContainsID", id)

    def GetCurveIDs(self):
        """
        Returns an array of Curve ID's for all the Curves in the group

        Returns
        -------
        list
            List of integers
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCurveIDs")

    def GetCurves(self):
        """
        Returns an array of Curve Objects for all the Curves in the group

        Returns
        -------
        list
            List of Curve objects
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCurves")

    def Remove(self, curve):
        """
        Removes a curve object from a group

        Parameters
        ----------
        curve : Curve
            Curve that will be removed from group

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Remove", curve)

    def RemoveAll(self):
        """
        Removes all curves from a group

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveAll")

    def RemoveID(self, id):
        """
        Remove a curve by ID from a group

        Parameters
        ----------
        id : integer
            The ID of the curve you want to remove

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveID", id)

    def Spool(self):
        """
        Spools a group, entry by entry and returns the curve objects. See also Group.StartSpool

        Returns
        -------
        Curve
            Curve Object of item, or None if no more curves in group
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Spool")

    def SpoolID(self):
        """
        Spools a group, entry by entry and returns the curve ID's or 0 when no more curves in group. See also Group.StartSpool

        Returns
        -------
        int
            integer
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "SpoolID")

    def StartSpool(self):
        """
        Starts a group spooling operation. See also Group.Spool

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "StartSpool")

