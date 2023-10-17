import Oasys.gRPC


# Metaclass for static properties and constants
class InterpolationSpotweldType(type):
    _consts = {'INVERSE', 'LINEAR', 'SPR3', 'SPR3_MAT_PARAM', 'SPR3_MAT_PARAM_MOD', 'SPR4', 'SPR4_MAT_PARAM', 'SPR4_MAT_PARAM_MOD', 'UNIFORM'}

    def __getattr__(cls, name):
        if name in InterpolationSpotweldType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class InterpolationSpotweld(Oasys.gRPC.OasysItem, metaclass=InterpolationSpotweldType):
    _props = {'alpha1', 'alpha2', 'alpha3', 'beta', 'beta2', 'beta3', 'dens', 'exists', 'gamma', 'include', 'intp', 'lcdexp', 'lcf', 'lcupf', 'lcupr', 'model', 'mrn', 'mrs', 'nsid', 'pid1', 'pid2', 'pidvb', 'r', 'rn', 'rs', 'scarn', 'scars', 'sropt', 'stf', 'stiff2', 'stiff3', 'stiff4', 'thick', 'upfn', 'upfs', 'uprn', 'uprs'}
    _rprops = {'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in InterpolationSpotweld._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in InterpolationSpotweld._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in InterpolationSpotweld._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in InterpolationSpotweld._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, pid1, pid2, nsid):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, pid1, pid2, nsid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model that all interpolation spotwelds will be blanked in
        redraw : boolean
            If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, redraw)

    def BlankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged interpolation spotwelds will be blanked in
        flag : Flag
            Flag set on the interpolation spotwelds that you want to blank
        redraw : boolean
            If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankFlagged", model, flag, redraw)

    def First(model):
        """
        Returns the first interpolation spotweld in the model

        Parameters
        ----------
        model : Model
            Model to get first interpolation spotweld in

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object (or None if there are no interpolation spotwelds in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the interpolation spotwelds in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all interpolation spotwelds will be flagged in
        flag : Flag
            Flag to set on the interpolation spotwelds

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns an array of InterpolationSpotweld objects for all of the interpolation spotwelds in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get interpolation spotwelds from

        Returns
        -------
        list
            List of InterpolationSpotweld objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns an array of InterpolationSpotweld objects for all of the flagged interpolation spotwelds in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get interpolation spotwelds from
        flag : Flag
            Flag set on the interpolation spotwelds that you want to retrieve

        Returns
        -------
        list
            List of InterpolationSpotweld objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the InterpolationSpotweld object for a interpolation spotweld ID

        Parameters
        ----------
        model : Model
            Model to find the interpolation spotweld in
        number : integer
            number of the interpolation spotweld you want the InterpolationSpotweld object for

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object (or None if interpolation spotweld does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last interpolation spotweld in the model

        Parameters
        ----------
        model : Model
            Model to get last interpolation spotweld in

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object (or None if there are no interpolation spotwelds in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a interpolation spotweld

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only interpolation spotwelds from that model can be picked.
            If the argument is a Flag then only interpolation spotwelds that
            are flagged with limit can be selected.
            If omitted, or null, any interpolation spotwelds from any model can be selected.
            from any model
        modal : boolean
            If picking is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the pick will be modal
        button_text : string
            By default the window with the prompt will have a button labelled 'Cancel'
            which if pressed will cancel the pick and return null. If you want to change the
            text on the button use this argument. If omitted 'Cancel' will be used

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select interpolation spotwelds using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting interpolation spotwelds
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only interpolation spotwelds from that model can be selected.
            If the argument is a Flag then only interpolation spotwelds that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any interpolation spotwelds can be selected.
            from any model
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of interpolation spotwelds selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged interpolation spotwelds in the model. The interpolation spotwelds will be sketched until you either call
        InterpolationSpotweld.Unsketch(),
        InterpolationSpotweld.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged interpolation spotwelds will be sketched in
        flag : Flag
            Flag set on the interpolation spotwelds that you want to sketch
        redraw : boolean
            If model should be redrawn or not after the interpolation spotwelds are sketched.
            If omitted redraw is true. If you want to sketch flagged interpolation spotwelds several times and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SketchFlagged", model, flag, redraw)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            true if only existing interpolation spotwelds should be counted. If false or omitted
            referenced but undefined interpolation spotwelds will also be included in the total

        Returns
        -------
        int
            number of interpolation spotwelds
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model that all interpolation spotwelds will be unblanked in
        redraw : boolean
            If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll", model, redraw)

    def UnblankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model that the flagged interpolation spotwelds will be unblanked in
        flag : Flag
            Flag set on the interpolation spotwelds that you want to unblank
        redraw : boolean
            If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankFlagged", model, flag, redraw)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all interpolation spotwelds will be unset in
        flag : Flag
            Flag to unset on the interpolation spotwelds

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all interpolation spotwelds

        Parameters
        ----------
        model : Model
            Model that all interpolation spotwelds will be unblanked in
        redraw : boolean
            If model should be redrawn or not after the interpolation spotwelds are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchAll", model, redraw)

    def UnsketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all flagged interpolation spotwelds in the model

        Parameters
        ----------
        model : Model
            Model that all interpolation spotwelds will be unsketched in
        flag : Flag
            Flag set on the interpolation spotwelds that you want to unsketch
        redraw : boolean
            If model should be redrawn or not after the interpolation spotwelds are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag, redraw)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a interpolation spotweld

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the interpolation spotweld

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the interpolation spotweld

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the interpolation spotweld is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the interpolation spotweld

        Parameters
        ----------
        flag : Flag
            Flag to clear on the interpolation spotweld

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the interpolation spotweld. The target include of the copied interpolation spotweld can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a interpolation spotweld

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the interpolation spotweld

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the interpolation spotweld is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the interpolation spotweld

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a interpolation spotweld

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a InterpolationSpotweld property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the InterpolationSpotweld.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            interpolation spotweld property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this interpolation spotweld (*CONSTRAINED_INTERPOLATION_SPOTWELD).
        Note that a carriage return is not added.
        See also InterpolationSpotweld.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the interpolation spotweld.
        Note that a carriage return is not added.
        See also InterpolationSpotweld.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next interpolation spotweld in the model

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object (or None if there are no more interpolation spotwelds in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous interpolation spotweld in the model

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object (or None if there are no more interpolation spotwelds in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the interpolation spotweld

        Parameters
        ----------
        flag : Flag
            Flag to set on the interpolation spotweld

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the interpolation spotweld. The interpolation spotweld will be sketched until you either call
        InterpolationSpotweld.Unsketch(),
        InterpolationSpotweld.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the interpolation spotweld is sketched.
            If omitted redraw is true. If you want to sketch several interpolation spotwelds and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unblank(self):
        """
        Unblanks the interpolation spotweld

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the interpolation spotweld

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the interpolation spotweld is unsketched.
            If omitted redraw is true. If you want to unsketch several interpolation spotwelds and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        InterpolationSpotweld
            InterpolationSpotweld object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this interpolation spotweld

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

