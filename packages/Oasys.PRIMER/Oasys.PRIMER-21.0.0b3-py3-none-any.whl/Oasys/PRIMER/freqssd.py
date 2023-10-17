import Oasys.gRPC


# Metaclass for static properties and constants
class FreqSSDType(type):
    _consts = {'DIRECT', 'DIRECT_FD', 'ERP', 'FATIGUE', 'FRF', 'SUBCASE'}

    def __getattr__(cls, name):
        if name in FreqSSDType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class FreqSSD(Oasys.gRPC.OasysItem, metaclass=FreqSSDType):
    _props = {'c', 'dampf', 'dmpflg', 'dmpmas', 'dmpstf', 'erpref', 'erprlf', 'exists', 'fnmax', 'fnmin', 'include', 'istress', 'label', 'lcdam', 'lcflag', 'lcftg', 'lctyp', 'mdmax', 'mdmin', 'memory', 'nerp', 'notyp', 'nout', 'nova', 'option', 'radeff', 'relatv', 'restdp', 'restmd', 'ro', 'strtyp'}
    _rprops = {'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in FreqSSD._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in FreqSSD._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in FreqSSD._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in FreqSSD._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a *FREQUENCY_DOMAIN_SSD card

        Parameters
        ----------
        model : Model
            Model that the *FREQUENCY_DOMAIN_SSD card will be created in
        modal : boolean
            If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first *FREQUENCY_DOMAIN_SSD in the model

        Parameters
        ----------
        model : Model
            Model to get first *FREQUENCY_DOMAIN_SSD in

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no *FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the *FREQUENCY_DOMAIN_SSDs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all *FREQUENCY_DOMAIN_SSDs will be flagged in
        flag : Flag
            Flag to set on the *FREQUENCY_DOMAIN_SSDs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns an array of FreqSSD objects for all of the *FREQUENCY_DOMAIN_SSDs in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get *FREQUENCY_DOMAIN_SSDs from

        Returns
        -------
        list
            List of FreqSSD objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetErpData(index):
        """
        Returns the ERP data for a specific ERP part as an array. For each ERP part there will be 2 values. 
        There are nerp ERP parts. This method is only applicable when option is
        FreqSSD.ERP.

        Parameters
        ----------
        index : integer
            Index you want the ERP data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the ERP data (values: pid[integer], ptyp[integer]). The array length will be 2
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetErpData", index)

    def GetFlagged(model, flag):
        """
        Returns an array of FreqSSD objects for all of the flagged *FREQUENCY_DOMAIN_SSDs in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get *FREQUENCY_DOMAIN_SSDs from
        flag : Flag
            Flag set on the *FREQUENCY_DOMAIN_SSDs that you want to retrieve

        Returns
        -------
        list
            List of FreqSSD objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the FreqSSD object for a *FREQUENCY_DOMAIN_SSD ID

        Parameters
        ----------
        model : Model
            Model to find the *FREQUENCY_DOMAIN_SSD in
        number : integer
            number of the *FREQUENCY_DOMAIN_SSD you want the FreqSSD object for

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if *FREQUENCY_DOMAIN_SSD does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def GetLoadData(index):
        """
        Returns the data for a specific excitation load as an array. For each load there will be 8
        values. There can be as many loads as needed. This method is only applicable when option is
        not FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want the load data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the load data (values: nid[integer], ntyp[integer], dof[integer], vad[integer],
            lc1[integer], lc2[integer], sf[real], vid[integer]). The array length will be 8.
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetLoadData", index)

    def GetSubcaseData(index):
        """
        Returns the data for a specific subcase as an array. For each subcase there will be 3 +
        8 x nload values. There can be as many subcases as needed. This method is only applicable when option is
        FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want the subcase data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the subcase data (values: caseid[string], title[string], nload[integer], nid[integer],
            ntyp[integer], dof[integer], vad[integer], lc1[integer], lc2[integer], sf[real], vid[integer], ...) 
            Where values nid to vid are repeated nload times in the array. The array length will be 3 + 8 x nload.
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetSubcaseData", index)

    def Last(model):
        """
        Returns the last *FREQUENCY_DOMAIN_SSD in the model

        Parameters
        ----------
        model : Model
            Model to get last *FREQUENCY_DOMAIN_SSD in

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no *FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select *FREQUENCY_DOMAIN_SSDs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting *FREQUENCY_DOMAIN_SSDs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only *FREQUENCY_DOMAIN_SSDs from that model can be selected.
            If the argument is a Flag then only *FREQUENCY_DOMAIN_SSDs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any *FREQUENCY_DOMAIN_SSDs can be selected.
            from any model
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of *FREQUENCY_DOMAIN_SSDs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SetErpData(index, data):
        """
        Set the data for a specific ERP part. For each ERP part there will be 2 values. 
        There are nerp ERP parts. This method is only applicable when option is
        FreqSSD.ERP.

        Parameters
        ----------
        index : integer
            Index you want to set ERP data for. Note that indices start at 0
        data : Array of data
            An array containing the ERP data (values: pid[integer], ptyp[integer]). The array length should be 2

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetErpData", index, data)

    def SetLoadData(index, data):
        """
        Set the data for a specific excitation load. For each load there will be 8 values. 
        There can be as many loads as needed. This method is only applicable when option is
        not FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want to set load data for. Note that indices start at 0
        data : Array of data
            An array containing the load data (values: nid[integer], ntyp[integer], dof[integer], vad[integer],
            lc1[integer], lc2[integer], sf[real], vid[integer]). The array length should be 8.

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetLoadData", index, data)

    def SetSubcaseData(index, caseid, title, nload, data):
        """
        Set the data for a specific subcase. For each subcase, data will have 8 x nload values.
        There can be as many subcases as needed. This method is only applicable when option is
        FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want to set subcase data for. Note that indices start at 0
        caseid : string
            Identification string to be used as the case ID (must include at least one letter)
        title : string
            A description of the current loading case (can be blank)
        nload : integer
            Number of loads for this loading case
        data : Array of data
            An array containing the subcase load data (values: nid[integer],
            ntyp[integer], dof[integer], vad[integer], lc1[integer], lc2[integer], sf[real], vid[integer], ...) 
            Where values nid to vid are repeated nload times in the array. The array length should be 8 x nload.

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetSubcaseData", index, caseid, title, nload, data)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of *FREQUENCY_DOMAIN_SSDs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            true if only existing *FREQUENCY_DOMAIN_SSDs should be counted. If false or omitted
            referenced but undefined *FREQUENCY_DOMAIN_SSDs will also be included in the total

        Returns
        -------
        int
            number of *FREQUENCY_DOMAIN_SSDs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the *FREQUENCY_DOMAIN_SSDs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all *FREQUENCY_DOMAIN_SSDs will be unset in
        flag : Flag
            Flag to unset on the *FREQUENCY_DOMAIN_SSDs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddLoadData(self):
        """
        Allows user to add a new load card in *FREQUENCY_DOMAIN_SSD. This method is only applicable when option is
        not FreqSSD.SUBCASE.
        The new card has uninitialised fields and should be updated by 
        FreqSSD.SetLoadData().

        Returns
        -------
        ?
            Index of the new load
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddLoadData")

    def AddSubcaseData(self):
        """
        Allows user to add new subcase cards in *FREQUENCY_DOMAIN_SSD. This method is only applicable when option is
        FreqSSD.SUBCASE.
        The new cards have uninitialised fields and should be updated by 
        FreqSSD.SetSubcaseData().

        Returns
        -------
        ?
            Index of the new subcase
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddSubcaseData")

    def AssociateComment(self, comment):
        """
        Associates a comment with a *FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Browse(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an edit panel in Browse mode

        Parameters
        ----------
        modal : boolean
            If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Browse", modal)

    def ClearFlag(self, flag):
        """
        Clears a flag on the *FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        flag : Flag
            Flag to clear on the *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the *FREQUENCY_DOMAIN_SSD. The target include of the copied *FREQUENCY_DOMAIN_SSD can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        FreqSSD
            FreqSSD object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a *FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Edit(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel

        Parameters
        ----------
        modal : boolean
            If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Edit", modal)

    def Flagged(self, flag):
        """
        Checks if the *FREQUENCY_DOMAIN_SSD is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a FreqSSD property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the FreqSSD.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            *FREQUENCY_DOMAIN_SSD property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this *FREQUENCY_DOMAIN_SSD.
        Note that a carriage return is not added.
        See also FreqSSD.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the *FREQUENCY_DOMAIN_SSD.
        Note that a carriage return is not added.
        See also FreqSSD.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next *FREQUENCY_DOMAIN_SSD in the model

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no more *FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous *FREQUENCY_DOMAIN_SSD in the model

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no more *FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveLoadData(self, index):
        """
        Allows user to remove a specified load card in *FREQUENCY_DOMAIN_SSD.
        This method is only applicable when option is not
        FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index of the load card you want to remove. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveLoadData", index)

    def RemoveSubcaseData(self, index):
        """
        Allows user to remove cards for a specified subcase in *FREQUENCY_DOMAIN_SSD.
        This method is only applicable when option is FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index of the subcase you want to remove cards for. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveSubcaseData", index)

    def SetFlag(self, flag):
        """
        Sets a flag on the *FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        flag : Flag
            Flag to set on the *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        FreqSSD
            FreqSSD object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this *FREQUENCY_DOMAIN_SSD

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

