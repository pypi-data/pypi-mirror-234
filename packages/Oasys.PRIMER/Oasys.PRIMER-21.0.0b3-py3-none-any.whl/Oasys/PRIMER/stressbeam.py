import Oasys.gRPC


# Metaclass for static properties and constants
class StressBeamType(type):
    _consts = {'GLOBAL_CSYS', 'LOCAL_CSYS', 'NAXES_0', 'NAXES_12', 'RULE_GUASS_QUADRATURE_NPTS_1', 'RULE_GUASS_QUADRATURE_NPTS_16', 'RULE_GUASS_QUADRATURE_NPTS_4', 'RULE_GUASS_QUADRATURE_NPTS_9', 'RULE_LOBATTO_QUADRATURE_NPTS_9'}

    def __getattr__(cls, name):
        if name in StressBeamType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class StressBeam(Oasys.gRPC.OasysItem, metaclass=StressBeamType):
    _props = {'eid', 'exists', 'include', 'large', 'local', 'naxes', 'nhisv', 'npts', 'rule'}
    _rprops = {'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in StressBeam._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in StressBeam._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in StressBeam._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in StressBeam._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, eid, rule, large=Oasys.gRPC.defaultArg, nhisv=Oasys.gRPC.defaultArg, local=Oasys.gRPC.defaultArg, naxes=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, eid, rule, large, nhisv, local, naxes)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first initial stress beam in the model

        Parameters
        ----------
        model : Model
            Model to get first initial stress beam in

        Returns
        -------
        StressBeam
            StressBeam object (or None if there are no initial stress beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the initial stress beams in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all initial stress beams will be flagged in
        flag : Flag
            Flag to set on the initial stress beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns an array of StressBeam objects for all of the initial stress beams in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get initial stress beams from

        Returns
        -------
        list
            List of StressBeam objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns an array of StressBeam objects for all of the flagged initial stress beams in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get initial stress beams from
        flag : Flag
            Flag set on the initial stress beams that you want to retrieve

        Returns
        -------
        list
            List of StressBeam objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the StressBeam object for a initial stress beam ID

        Parameters
        ----------
        model : Model
            Model to find the initial stress beam in
        number : integer
            number of the initial stress beam you want the StressBeam object for

        Returns
        -------
        StressBeam
            StressBeam object (or None if initial stress beam does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last initial stress beam in the model

        Parameters
        ----------
        model : Model
            Model to get last initial stress beam in

        Returns
        -------
        StressBeam
            StressBeam object (or None if there are no initial stress beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a initial stress beam

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only initial stress beams from that model can be picked.
            If the argument is a Flag then only initial stress beams that
            are flagged with limit can be selected.
            If omitted, or null, any initial stress beams from any model can be selected.
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
        StressBeam
            StressBeam object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select initial stress beams using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting initial stress beams
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only initial stress beams from that model can be selected.
            If the argument is a Flag then only initial stress beams that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any initial stress beams can be selected.
            from any model
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of initial stress beams selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged initial stress beams in the model. The initial stress beams will be sketched until you either call
        StressBeam.Unsketch(),
        StressBeam.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial stress beams will be sketched in
        flag : Flag
            Flag set on the initial stress beams that you want to sketch
        redraw : boolean
            If model should be redrawn or not after the initial stress beams are sketched.
            If omitted redraw is true. If you want to sketch flagged initial stress beams several times and only
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
        Returns the total number of initial stress beams in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            true if only existing initial stress beams should be counted. If false or omitted
            referenced but undefined initial stress beams will also be included in the total

        Returns
        -------
        int
            number of initial stress beams
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the initial stress beams in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all initial stress beams will be unset in
        flag : Flag
            Flag to unset on the initial stress beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all initial stress beams

        Parameters
        ----------
        model : Model
            Model that all initial stress beams will be unblanked in
        redraw : boolean
            If model should be redrawn or not after the initial stress beams are unsketched.
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
        Unsketches all flagged initial stress beams in the model

        Parameters
        ----------
        model : Model
            Model that all initial stress beams will be unsketched in
        flag : Flag
            Flag set on the initial stress beams that you want to unsketch
        redraw : boolean
            If model should be redrawn or not after the initial stress beams are unsketched.
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
        Associates a comment with a initial stress beam

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the initial stress beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def ClearFlag(self, flag):
        """
        Clears a flag on the initial stress beam

        Parameters
        ----------
        flag : Flag
            Flag to clear on the initial stress beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the initial stress beam. The target include of the copied initial stress beam can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        StressBeam
            StressBeam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a initial stress beam

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the initial stress beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the initial stress beam is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the initial stress beam

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a initial stress beam

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetIntegrationPoint(self, index):
        """
        Returns the data for a specific integration point as an array. 
        For each integration point there will be 7 values if large is FALSE.
        For each integration point there will be (7 + nhisv) values if large is TRUE.
        There are npts integration points

        Parameters
        ----------
        index : integer
            Index you want the integration point data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the integration point data
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetIntegrationPoint", index)

    def GetLocalAxesValues(self):
        """
        Returns the 12 axes values as an array. The axes values are valid only if the 
        naxes is set to StressBeam.NAXES_12

        Returns
        -------
        list
            A list containing the axes values
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLocalAxesValues")

    def GetParameter(self, prop):
        """
        Checks if a StressBeam property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the StressBeam.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            initial stress beam property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this initial stress beam (*INITIAL_STRESS_BEAM).
        Note that a carriage return is not added.
        See also StressBeam.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the initial stress beam.
        Note that a carriage return is not added.
        See also StressBeam.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next initial stress beam in the model

        Returns
        -------
        StressBeam
            StressBeam object (or None if there are no more initial stress beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous initial stress beam in the model

        Returns
        -------
        StressBeam
            StressBeam object (or None if there are no more initial stress beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the initial stress beam

        Parameters
        ----------
        flag : Flag
            Flag to set on the initial stress beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetIntegrationPoint(self, index, data):
        """
        Set the data for a specific integration point. 
        For each integration point there will be 7 values if large is FALSE.
        For each integration point there will be (7 + nhisv) values if large is TRUE.
        There are npts integration points

        Parameters
        ----------
        index : integer
            Index you want the integration point data for. Note that indices start at 0
        data : Array of data
            Array containing the integration point data. 
            The array length should be 7 if large is FALSE.
            The array length should be (7 + nhisv) if large is TRUE

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetIntegrationPoint", index, data)

    def SetLocalAxesValues(self, data):
        """
        Sets the 12 axes values as an array. The axes values are set only if the 
        naxes is set to StressBeam.NAXES_12

        Parameters
        ----------
        data : Array of data
            Array containing the axes values data. The array length should be 12

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetLocalAxesValues", data)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the initial stress beam. The initial stress beam will be sketched until you either call
        StressBeam.Unsketch(),
        StressBeam.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the initial stress beam is sketched.
            If omitted redraw is true. If you want to sketch several initial stress beams and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the initial stress beam

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the initial stress beam is unsketched.
            If omitted redraw is true. If you want to unsketch several initial stress beams and only
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
        StressBeam
            StressBeam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this initial stress beam

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

