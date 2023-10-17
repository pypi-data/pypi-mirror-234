import Oasys.gRPC


# Metaclass for static properties and constants
class ModelType(type):
    _consts = {'ALL_FILES', 'ASCII', 'LSDA', 'THF', 'XTF', 'ZTF'}

    def __getattr__(cls, name):
        if name in ModelType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Model(Oasys.gRPC.OasysItem, metaclass=ModelType):
    _props = {'dir', 'file', 'id', 'title'}


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Model._props:
            return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Model._props:
            Oasys.THIS._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Exists(model_number):
        """
        Checks if a model exists

        Parameters
        ----------
        model_number : integer
            The number of the model you want to check the existence of

        Returns
        -------
        bool
            True if the model exists, otherwise False
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Exists", model_number)

    def GetFromID(model_number):
        """
        Returns the Model object for a model ID or null if model does not exist

        Parameters
        ----------
        model_number : integer
            number of the model you want the Model object for

        Returns
        -------
        Model
            Model object (or None if model does not exist)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "GetFromID", model_number)

    def HighestID():
        """
        Returns the ID of the highest model currently being used

        Returns
        -------
        int
            ID of highest model currently being used
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "HighestID")

    def Read(filename, filetype=Oasys.gRPC.defaultArg):
        """
        Reads in a new model

        Parameters
        ----------
        filename : string
            Filename you want to read
        filetype : integer
            Filetypes you want to read. Can be bitwise OR of Model.THF, 
            Model.XTF, Model.LSDA, Model.ASCII, Model.ZTF and Model.ALL_FILES. 
            If omitted all available files will be read

        Returns
        -------
        Model
            Model object (or None if error)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Read", filename, filetype)

    def Total():
        """
        Returns the total number of models

        Returns
        -------
        int
            integer
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def ClearFlag(self, flag, entity_type, item, end=Oasys.gRPC.defaultArg):
        """
        Clears a defined flag on an internal (or external) item(s) of type of entity_type in the model

        Parameters
        ----------
        flag : Flag
            The flag you want to clear
        entity_type : integer
            The Entity type that the defined flag will be cleared on
        item : integer
            If +ive: The internal item number starting from 1. If -ive: The external item label
        end : integer
            To unflag range of items, specify an optional end of range. Unflags items from item to range

        Returns
        -------
        bool
            True if the flag is successfully cleared on the item, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag, entity_type, item, end)

    def Delete(self):
        """
        Deletes a model
        Do not use the Model object after calling this method

        Returns
        -------
        bool
            True if the model sucessfully deleted, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def FlagAll(self, flag, entity_type):
        """
        Sets a defined flag on all of items of type of entity_type in the model

        Parameters
        ----------
        flag : Flag
            The flag you want to set
        entity_type : integer
            The Entity type that the defined flag will be set on

        Returns
        -------
        bool
            True if the flag is successfully set on all the items, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "FlagAll", flag, entity_type)

    def Flagged(self, flag, entity_type, item):
        """
        Checks if a defined flag is set on an internal (or external) item of type of entity_type in the model

        Parameters
        ----------
        flag : Flag
            The flag you want to check
        entity_type : integer
            The Entity type to check
        item : integer
            If +ive: The internal item number starting from 1. If -ive: The external item label

        Returns
        -------
        bool
            True if the flag is set, False if the flag is not set
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag, entity_type, item)

    def GetDataFlagged(self, flag, data_comp, int_pnt=Oasys.gRPC.defaultArg, extra=Oasys.gRPC.defaultArg):
        """
        Gets curve objects for a data component for relevant items that are flagged with a specified flag in the model. 
        Some data components are valid for different entity types (e.g. SXX). If the same flag is set on items of different entity types, data is returned for all relevant, flagged entity types. 
        To return the same data for multiple items of the same type, it will be much faster if you flag all items you want data for, and do a single call to GetDataFlagged(). 
        The curves are ordered by type, then by the ascending internal index of the items. Use curve properties to identify which curve is which.
        If the data is not available in the model for a flagged item, or not available for the selected integration points or extra value, a curve is not returned.
        You can use QueryDataPresent() to check if the data is available.
        It is recommended that you check the number of curves returned. This can be compared with the number of flagged entities, 
        see GetNumberFlagged().
        If the data is generally available in the model, but not for the specific flagged item, a "null curve" which contains no x-y data values is returned.
        For example, a specific shell may have fewer integration points than MAX_INT for all shells, a "null curve" would be returned for the higher integration points.

        Parameters
        ----------
        flag : Flag
            The flag to use. For model data, use 0 to define a null "padding" argument
        data_comp : integer
            The Data Component to extract
        int_pnt : dict
            The integration points to extract. This argument is ignored when the entity type is not SOLID, SHELL, THICK_SHELL or BEAM.
            An integer specifies the integration point to extract:
            For SOLIDs: value between 0 for Average/Centre and 8. (Defaults to Average/Centre).
            For SHELLs and THICK_SHELLs: value between 1 and # integration points, or codes TOP, MIDDLE, BOTTOM. (Defaults to MIDDLE integration point). 
            For integrated BEAMs: value between 1 and # integration points. (Defaults to integration point 1).
            Use 0 to define a null "padding" argument, then uses the default integration point
        extra : integer
            The extra component id for SOLIDs, SHELLs, THICK_SHELLs or BEAMs

        Returns
        -------
        list
            List of Curve objects
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetDataFlagged", flag, data_comp, int_pnt, extra)

    def GetInternalID(self, entity_type, item):
        """
        Gets the internal ID of external item of type entity_type in the model

        Parameters
        ----------
        entity_type : integer
            The Entity type of the item
        item : integer
            The external item number

        Returns
        -------
        int
            Integer internal ID (starting from 1) with reference to the entity_type code. Returns integer internal ID of 0 if item cannot be found
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetInternalID", entity_type, item)

    def GetLabel(self, entity_type, item):
        """
        Gets the external label of internal item of type entity_type in the model

        Parameters
        ----------
        entity_type : integer
            The Entity type of the item
        item : integer
            The internal item number starting from 1

        Returns
        -------
        int
            Integer external ID (or 0 if there is an error, or the internal ID if there are no external IDs)
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLabel", entity_type, item)

    def GetLabelFromName(self, entity_type, name):
        """
        Gets the external label from the database history name name of type entity_type in the model. 
        This is quicker if you use parent entity type codes (e.g. Entity.WELD rather than Entity.WELD_CONSTRAINED)

        Parameters
        ----------
        entity_type : integer
            The Entity type of the item
        name : string
            The name of the item. If only the first part of the name is given, it must be unambiguous

        Returns
        -------
        int
            Integer external ID of the first matching name (or 0 if there is an error)
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLabelFromName", entity_type, name)

    def GetName(self, entity_type, item):
        """
        Gets the database history name of an internal (or external) item of type entity_type in the model

        Parameters
        ----------
        entity_type : integer
            The Entity type of the item
        item : integer
            If +ive: The internal item number starting from 1. If -ive: The external item label

        Returns
        -------
        str
            String containing the database history name (or None if not available)
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetName", entity_type, item)

    def GetNumberFlagged(self, flag, entity_type=Oasys.gRPC.defaultArg):
        """
        Gets the number of entities flagged with a requested flag in the model

        Parameters
        ----------
        flag : Flag
            The flag you want to check
        entity_type : integer
            If specified, the Entity type to look at. If not specified, all types are looked at

        Returns
        -------
        int
            Integer number
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNumberFlagged", flag, entity_type)

    def GetNumberOf(self, entity_type):
        """
        Gets the number of entities of a requested type in the model

        Parameters
        ----------
        entity_type : integer
            The Entity type that you want to know the number of

        Returns
        -------
        int
            Integer number
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNumberOf", entity_type)

    def QueryDataPresent(self, data_comp, entity_type=Oasys.gRPC.defaultArg, int_pnt=Oasys.gRPC.defaultArg, extra=Oasys.gRPC.defaultArg):
        """
        Checks if a data component data_comp for a given entity is present in a model's database.
        For SOLIDs, SHELLs, THICK_SHELLs and BEAMs the integration point and extra component ID can also be checked.
        This will show if curves for any flagged items of this type will be returned for GetDataFlagged(). 
        Note, it does not check if the data component is valid, for example a specific shell may have fewer integration points than MAX_INT for all shells, 
        so curves returned for GetDataFlagged() may still be "null" with no x-y data

        Parameters
        ----------
        data_comp : integer
            The Data Component to check
        entity_type : integer
            The Entity type to check. This argument can only be omitted when checking for global model data
        int_pnt : dict
            The integration points to check. This argument is ignored if the entity type is not SOLID, SHELL, THICK_SHELL or BEAM.
            An integer specifies the integration point to check:
            For SOLIDs: value between 0 for Average/Centre and 8. (Defaults to Average/Centre).
            For SHELLs and THICK_SHELLs: value between 1 and # integration points, or codes TOP, MIDDLE, BOTTOM. (Defaults to MIDDLE integration point). 
            For integrated BEAMs: value between 1 and # integration points. (Defaults to integration point 1).
            Use 0 to define a null "padding" argument, then checks the default integration point
        extra : integer
            The extra component id for SOLIDs, SHELLs, THICK_SHELLs or BEAMs

        Returns
        -------
        bool
            JS_True if data is present, otherwise JS_False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "QueryDataPresent", data_comp, entity_type, int_pnt, extra)

    def SetFlag(self, flag, entity_type, item, end=Oasys.gRPC.defaultArg):
        """
        Sets a defined flag on an internal (or external) item(s) of type of entity_type in the model

        Parameters
        ----------
        flag : Flag
            The flag you want to set
        entity_type : integer
            The Entity type that the defined flag will be set on
        item : integer
            If +ive: The internal item number starting from 1. If -ive: The external item label
        end : integer
            To flag range of items, specify an optional end of range. Flags items from item to range

        Returns
        -------
        bool
            True if the flag is successfully set on the item, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag, entity_type, item, end)

    def UnflagAll(self, flag, entity_type):
        """
        Unsets a defined flag flag on all of items of type of entity_type in the model

        Parameters
        ----------
        flag : Flag
            The flag you want to unset
        entity_type : integer
            The Entity type that the defined flag will be unset on

        Returns
        -------
        bool
            True if the flag is successfully unset on all the items, otherwise False
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "UnflagAll", flag, entity_type)

