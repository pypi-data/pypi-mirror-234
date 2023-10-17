import Oasys.gRPC


# Metaclass for static properties and constants
class FreqFRFType(type):
    _consts = {'NODE', 'NODE_SET', 'SEGMENT_SET'}

    def __getattr__(cls, name):
        if name in FreqFRFType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class FreqFRF(Oasys.gRPC.OasysItem, metaclass=FreqFRFType):
    _props = {'dampf', 'dmpmas', 'dmpstf', 'dof1', 'dof2', 'exists', 'fmax', 'fmin', 'fnmax', 'fspace', 'include', 'label', 'lcdam', 'lcfreq', 'lctyp', 'mdmax', 'mdmin', 'n1', 'n1typ', 'n2', 'n2typ', 'nfreq', 'output', 'relatv', 'restrt', 'vad1', 'vad2', 'vid1', 'vid2'}
    _rprops = {'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in FreqFRF._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in FreqFRF._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in FreqFRF._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in FreqFRF._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, n1, n1typ, n2, n2typ):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, n1, n1typ, n2, n2typ)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first *FREQUENCY_DOMAIN_FRF in the model

        Parameters
        ----------
        model : Model
            Model to get first *FREQUENCY_DOMAIN_FRF in

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no *FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the *FREQUENCY_DOMAIN_FRFs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all *FREQUENCY_DOMAIN_FRFs will be flagged in
        flag : Flag
            Flag to set on the *FREQUENCY_DOMAIN_FRFs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns an array of FreqFRF objects for all of the *FREQUENCY_DOMAIN_FRFs in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get *FREQUENCY_DOMAIN_FRFs from

        Returns
        -------
        list
            List of FreqFRF objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns an array of FreqFRF objects for all of the flagged *FREQUENCY_DOMAIN_FRFs in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get *FREQUENCY_DOMAIN_FRFs from
        flag : Flag
            Flag set on the *FREQUENCY_DOMAIN_FRFs that you want to retrieve

        Returns
        -------
        list
            List of FreqFRF objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the FreqFRF object for a *FREQUENCY_DOMAIN_FRF ID

        Parameters
        ----------
        model : Model
            Model to find the *FREQUENCY_DOMAIN_FRF in
        number : integer
            number of the *FREQUENCY_DOMAIN_FRF you want the FreqFRF object for

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if *FREQUENCY_DOMAIN_FRF does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last *FREQUENCY_DOMAIN_FRF in the model

        Parameters
        ----------
        model : Model
            Model to get last *FREQUENCY_DOMAIN_FRF in

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no *FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select *FREQUENCY_DOMAIN_FRFs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting *FREQUENCY_DOMAIN_FRFs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only *FREQUENCY_DOMAIN_FRFs from that model can be selected.
            If the argument is a Flag then only *FREQUENCY_DOMAIN_FRFs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any *FREQUENCY_DOMAIN_FRFs can be selected.
            from any model
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of *FREQUENCY_DOMAIN_FRFs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of *FREQUENCY_DOMAIN_FRFs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            true if only existing *FREQUENCY_DOMAIN_FRFs should be counted. If false or omitted
            referenced but undefined *FREQUENCY_DOMAIN_FRFs will also be included in the total

        Returns
        -------
        int
            number of *FREQUENCY_DOMAIN_FRFs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the *FREQUENCY_DOMAIN_FRFs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all *FREQUENCY_DOMAIN_FRFs will be unset in
        flag : Flag
            Flag to unset on the *FREQUENCY_DOMAIN_FRFs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a *FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the *FREQUENCY_DOMAIN_FRF

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
        Clears a flag on the *FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        flag : Flag
            Flag to clear on the *FREQUENCY_DOMAIN_FRF

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the *FREQUENCY_DOMAIN_FRF. The target include of the copied *FREQUENCY_DOMAIN_FRF can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        FreqFRF
            FreqFRF object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a *FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the *FREQUENCY_DOMAIN_FRF

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
        Checks if the *FREQUENCY_DOMAIN_FRF is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the *FREQUENCY_DOMAIN_FRF

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a *FREQUENCY_DOMAIN_FRF

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a FreqFRF property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the FreqFRF.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            *FREQUENCY_DOMAIN_FRF property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this *FREQUENCY_DOMAIN_FRF
        Note that a carriage return is not added.
        See also FreqFRF.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the *FREQUENCY_DOMAIN_FRF.
        Note that a carriage return is not added.
        See also FreqFRF.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next *FREQUENCY_DOMAIN_FRF in the model

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no more *FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous *FREQUENCY_DOMAIN_FRF in the model

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no more *FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the *FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        flag : Flag
            Flag to set on the *FREQUENCY_DOMAIN_FRF

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
        FreqFRF
            FreqFRF object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this *FREQUENCY_DOMAIN_FRF

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

