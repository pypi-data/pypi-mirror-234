import Oasys.gRPC


# Metaclass for static properties and constants
class ConxType(type):
    _consts = {'ADHESIVE', 'ADHESIVE_PATCH', 'ADHESIVE_SOLID', 'ASSEMBLY', 'BAD', 'BOLT', 'BOLT_MODULE', 'BOLT_MRG_2PTS', 'BOLT_MRG_2PTS_RB', 'BOLT_MRG_2PTS_RJ', 'BOLT_MRG_CYL', 'BOLT_MRG_CYL_BALL', 'BOLT_MRG_CYL_BEAM', 'BOLT_NRB_2PTS', 'BOLT_NRB_CYL', 'BOLT_NRB_CYL_BALL', 'BOLT_NRB_CYL_BEAM', 'BOLT_NRB_SPH', 'BOLT_NRB_SPH_BALL', 'BOLT_NRB_SPH_DISC', 'DORMANT', 'INVALID', 'MADE', 'PART_SET', 'REALIZED', 'RIVET', 'SPOTWELD', 'SPOTWELD_BEAM', 'SPOTWELD_LINE', 'SPOTWELD_MIG', 'SPOTWELD_SOLID1', 'SPOTWELD_SOLID12', 'SPOTWELD_SOLID16', 'SPOTWELD_SOLID4', 'SPOTWELD_SOLID8'}

    def __getattr__(cls, name):
        if name in ConxType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Conx(Oasys.gRPC.OasysItem, metaclass=ConxType):
    _props = {'adhesive_esize', 'adhesive_nelem', 'adhesive_width', 'angtol', 'angtol2', 'assembly', 'assembly_type', 'colour', 'diameter', 'diameter2', 'edge_distance', 'edge_lock', 'error', 'error_details', 'fit', 'id', 'include', 'label', 'layers', 'length', 'length2', 'material', 'module', 'part', 'patch_coords', 'patch_topol', 'path', 'pitch', 'resize', 'saved_settings', 'shape', 'shape2', 'spr2_id', 'spr2_match', 'spr2_unshared', 'status', 'subtype', 'title', 'transparency', 'type', 'user_data', 'x', 'x2', 'y', 'y2', 'z', 'z2'}
    _rprops = {'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Conx._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Conx._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Conx._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Conx._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, x, y, z, type=Oasys.gRPC.defaultArg, subtype=Oasys.gRPC.defaultArg, title=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, x, y, z, type, subtype, title)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the connections in the model

        Parameters
        ----------
        model : Model
            Model that all connections will be blanked in
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
        Blanks all of the flagged connections in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged connections will be blanked in
        flag : Flag
            Flag set on the connections that you want to blank
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
        Returns the first connection in the model

        Parameters
        ----------
        model : Model
            Model to get first connection in

        Returns
        -------
        Conx
            Conx object (or None if there are no connections in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free connection label in the model.
        Also see Conx.LastFreeLabel(),
        Conx.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free connection label in
        layer : Include number
            Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Conx label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the connections in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all connections will be flagged in
        flag : Flag
            Flag to set on the connections

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns an array of Conx objects for all of the connections in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get connections from

        Returns
        -------
        list
            List of Conx objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns an array of Conx objects for all of the flagged connections in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get connections from
        flag : Flag
            Flag set on the connections that you want to retrieve

        Returns
        -------
        list
            List of Conx objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the Conx object for a connection ID

        Parameters
        ----------
        model : Model
            Model to find the connection in
        number : integer
            number of the connection you want the Conx object for

        Returns
        -------
        Conx
            Conx object (or None if connection does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last connection in the model

        Parameters
        ----------
        model : Model
            Model to get last connection in

        Returns
        -------
        Conx
            Conx object (or None if there are no connections in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free connection label in the model.
        Also see Conx.FirstFreeLabel(),
        Conx.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free connection label in
        layer : Include number
            Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Conx label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) connection label in the model.
        Also see Conx.FirstFreeLabel(),
        Conx.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free connection label in
        layer : Include number
            Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Conx label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a connection

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only connections from that model can be picked.
            If the argument is a Flag then only connections that
            are flagged with limit can be selected.
            If omitted, or null, any connections from any model can be selected.
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
        Conx
            Conx object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RealizeAll(model):
        """
        Realizes all of the connections in the model

        Parameters
        ----------
        model : Model
            Model that all connections will be realized in

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RealizeAll", model)

    def RealizeFlagged(model, flag):
        """
        Realizes all of the flagged connections in the model

        Parameters
        ----------
        model : Model
            Model that the flagged connections will be realized in
        flag : Flag
            Flag set on the connections that you want to realize

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RealizeFlagged", model, flag)

    def ReloadConnectors():
        """
        Reload all modules from primer_library/connectors

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "ReloadConnectors")

    def RenumberAll(model, start):
        """
        Renumbers all of the connections in the model

        Parameters
        ----------
        model : Model
            Model that all connections will be renumbered in
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberAll", model, start)

    def RenumberFlagged(model, flag, start):
        """
        Renumbers all of the flagged connections in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged connections will be renumbered in
        flag : Flag
            Flag set on the connections that you want to renumber
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberFlagged", model, flag, start)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select connections using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting connections
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only connections from that model can be selected.
            If the argument is a Flag then only connections that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any connections can be selected.
            from any model
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of connections selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SetRuleDiameter(diameter):
        """
        Set the diameter for a spotweld ring when running a rule. Note that this method
        can only be called when running a connection rule script. It will not have any effect if
        used in a 'normal' script

        Parameters
        ----------
        diameter : integer
            The diameter to set for the ring

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetRuleDiameter", diameter)

    def SetRuleFEPID(pid):
        """
        Set the PID for spotweld beam/solid elements or adhesive solids when running a rule. Note that this method
        can only be called when running a connection rule script. It will not have any effect if
        used in a 'normal' script

        Parameters
        ----------
        pid : integer
            The PID to set for the spotweld or adhesive elements

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetRuleFEPID", pid)

    def SetRulePID(pid):
        """
        Set the PID for a spotweld ring when running a rule. Note that this method
        can only be called when running a connection rule script. It will not have any effect if
        used in a 'normal' script

        Parameters
        ----------
        pid : integer
            The PID to set for the ring

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetRulePID", pid)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged connections in the model. The connections will be sketched until you either call
        Conx.Unsketch(),
        Conx.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged connections will be sketched in
        flag : Flag
            Flag set on the connections that you want to sketch
        redraw : boolean
            If model should be redrawn or not after the connections are sketched.
            If omitted redraw is true. If you want to sketch flagged connections several times and only
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
        Returns the total number of connections in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            true if only existing connections should be counted. If false or omitted
            referenced but undefined connections will also be included in the total

        Returns
        -------
        int
            number of connections
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the connections in the model

        Parameters
        ----------
        model : Model
            Model that all connections will be unblanked in
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
        Unblanks all of the flagged connections in the model

        Parameters
        ----------
        model : Model
            Model that the flagged connections will be unblanked in
        flag : Flag
            Flag set on the connections that you want to unblank
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
        Unsets a defined flag on all of the connections in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all connections will be unset in
        flag : Flag
            Flag to unset on the connections

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all connections

        Parameters
        ----------
        model : Model
            Model that all connections will be unblanked in
        redraw : boolean
            If model should be redrawn or not after the connections are unsketched.
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
        Unsketches all flagged connections in the model

        Parameters
        ----------
        model : Model
            Model that all connections will be unsketched in
        flag : Flag
            Flag set on the connections that you want to unsketch
        redraw : boolean
            If model should be redrawn or not after the connections are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag, redraw)

    def UseParentLayer(option):
        """
        True (default) means put bolt FE into parent layer where possible

        Parameters
        ----------
        option : boolean
            True (default) means put bolt FE into parent layer where possible

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UseParentLayer", option)

    def UseSPR2Pref(option):
        """
        True (default) means use the pref settings for C_SPR2 created when rivet realized

        Parameters
        ----------
        option : boolean
            True (default) means use the pref settings for C_SPR2 created when rivet realized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UseSPR2Pref", option)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a connection

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the connection

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the connection

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the connection is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the connection

        Parameters
        ----------
        flag : Flag
            Flag to clear on the connection

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the connection. The target include of the copied connection can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Conx
            Conx object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a connection

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the connection

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def EmptyPatch(self):
        """
        Empties the patch topology/coordinates data

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "EmptyPatch")

    def ExtractColour(self):
        """
        Extracts the actual colour used for connection.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the connection colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the connection

        Returns
        -------
        ?
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the connection is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the connection

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a connection

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetElements(self):
        """
        Returns the beams/solids that are used in the connection weld

        Returns
        -------
        list
            A list containing the element IDs (or None if no elements)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetElements")

    def GetEntities(self, type):
        """
        Returns list of the entities of type that are used in the connection

        Parameters
        ----------
        type : string
            The type of the item in the reference list (for a list of types see Appendix I of the PRIMER manual)

        Returns
        -------
        list
            A list containing the item IDs (or None if none)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetEntities", type)

    def GetLayerData(self, layer):
        """
        Returns the data for a layer of the connection

        Parameters
        ----------
        layer : integer
            The layer you want the data for. Note that layers start at 0, not 1

        Returns
        -------
        list
            A list containing the layer data
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLayerData", layer)

    def GetLayerShells(self, layer):
        """
        Returns the attached shells for a layer of the connection

        Parameters
        ----------
        layer : integer
            The layer you want the data for. Note that layers start at 0, not 1

        Returns
        -------
        list
            List of Shell objects or None if not valid
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLayerShells", layer)

    def GetParameter(self, prop):
        """
        Checks if a Conx property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Conx.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            connection property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPatchCoords(self, point):
        """
        Returns the data for a patch coordinate of an adhesive patch connection

        Parameters
        ----------
        point : integer
            The point you want the data for. Note that points start at 0, not 1

        Returns
        -------
        list
            A list containing the patch coordinate
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPatchCoords", point)

    def GetPatchTopol(self, point):
        """
        Returns the topology for a patch quad/tria of an adhesive patch connection

        Parameters
        ----------
        point : integer
            The patch quad/tria you want the data for. Note that points start at 0, not 1

        Returns
        -------
        list
            List of numbers containing the patch topology information
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPatchTopol", point)

    def GetPathData(self, point):
        """
        Returns the data for a path point of an adhesive/spotweld line connection

        Parameters
        ----------
        point : integer
            The point you want the data for. Note that points start at 0, not 1

        Returns
        -------
        list
            A list containing the path data
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPathData", point)

    def GetPidData(self):
        """
        Returns an array of Part objects for the connection FE entities. A connection can
        contain elements with different part ID's between different layers. If one
        part ID is returned, that part is used for all elements in the connection. Not applicable for bolts

        Returns
        -------
        list
            List of Part objects
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPidData")

    def GetSettings(self):
        """
        Returns an object of settings stored with the connection

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetSettings")

    def GetShellThickness(self, layer):
        """
        Returns an array containing a number of objects equal to the number of solid elements in the connection. Each object
        contains the corresponding solid element object, and shell element objects and their thicknesses. The argument allows
        the user to output only shells from all layers, or a particular layer. 
        Note that a carriage return is not added

        Parameters
        ----------
        layer : integer
            ID of the connection layer containing the shells from which the thicknesses will be extracted. 
            If a value of zero or lower is input, all layers will be considered in the output data

        Returns
        -------
        list
            An array containing a number of objects equal to the number of solid elements in the connection. Each object has the following properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetShellThickness", layer)

    def Keyword(self):
        """
        Returns the keyword for this connection (*CONNECTION_START_SPOTWELD etc).
        Note that a carriage return is not added.
        See also Conx.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the connection.
        Note that a carriage return is not added.
        See also Conx.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next connection in the model

        Returns
        -------
        Conx
            Conx object (or None if there are no more connections in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous connection in the model

        Returns
        -------
        Conx
            Conx object (or None if there are no more connections in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemovePatchTopol(self, layer):
        """
        Deletes the topology at a particular location for patch type adhesive

        Parameters
        ----------
        layer : integer
            The topology location you want to remove. Note that layers start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePatchTopol", layer)

    def RemovePathData(self, layer):
        """
        Deletes a pathc point for a line adhesive connection

        Parameters
        ----------
        layer : integer
            The point you want to remove. Note that layers start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePathData", layer)

    def SetFlag(self, flag):
        """
        Sets a flag on the connection

        Parameters
        ----------
        flag : Flag
            Flag to set on the connection

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetLayerData(self, layer, item1, item2=Oasys.gRPC.defaultArg, _=Oasys.gRPC.defaultArg):
        """
        Sets the data for a layer of the connection

        Parameters
        ----------
        layer : integer
            The layer you want to set the data for. Note that layers start at 0, not 1
        item1 : integer/string
            The first item for the layer definition. As layer definitions can be part IDs,
            part names, CAD names, part set IDs, part set names or assemby names the following logic is used.
            If the item is an integer it is assumed to be a part ID. If the item is a string then it must be
            in the format 'P<part ID>', 'P:<part name>', 'C:<CAD name>', 'S<set ID>',
            'S:<set name>'
            or 'A:<assembly name>'
        item2 : integer/string
            The second item for the layer definition. This must be type same type as
            item1. e.g. if item1 is a part ID, item2 must be a part ID (it cannot be a part name etc).
        _ : integer/string
            The nth item for the layer definition. This must be type same type as
            item1. e.g. if item1 is a part ID, this item must be a part ID (it cannot be a part name etc).

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetLayerData", layer, item1, item2, _)

    def SetPatchCoords(self, point, x, y, z):
        """
        Sets a coordinate used by the adhesive patch connection type

        Parameters
        ----------
        point : integer
            The point you want to set the data for. Note that points start at 0, not 1
        x : float
            X coordinate of point
        y : float
            Y coordinate of point
        z : float
            Z coordinate of point

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPatchCoords", point, x, y, z)

    def SetPatchTopol(self, point, c1, c2, c3, c4=Oasys.gRPC.defaultArg):
        """
        Sets the topology used by the adhesive patch connection type

        Parameters
        ----------
        point : integer
            The point you want to set the data for. Note that points start at 0, not 1
        c1 : integer
            1st coordinate location point
        c2 : integer
            2nd coordinate location point
        c3 : integer
            3rd coordinate location point
        c4 : integer
            4th coordinate location point

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPatchTopol", point, c1, c2, c3, c4)

    def SetPathData(self, point, x, y, z):
        """
        Sets the data for a path point of the connection

        Parameters
        ----------
        point : integer
            The point you want to set the data for. Note that points start at 0, not 1
        x : float
            X coordinate of point
        y : float
            Y coordinate of point
        z : float
            Z coordinate of point

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPathData", point, x, y, z)

    def SetPidData(self, item1, item2=Oasys.gRPC.defaultArg, _=Oasys.gRPC.defaultArg):
        """
        Sets the element part IDs for the connection. A different part can be defined for
        elements in the connection between different layers. Not applicable for bolts

        Parameters
        ----------
        item1 : integer/string
            Part label of the first item in the PID layer list
        item2 : integer/string
            The second item for the layer definition
        _ : integer/string
            The nth item for the layer definition

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPidData", item1, item2, _)

    def SetSettings(self, data):
        """
        Sets the settings stored on a connection entity. Not applicable for bolts

        Parameters
        ----------
        data : dict
            Object containing the connection settings data. The properties can be:

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetSettings", data)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the connection. The connection will be sketched until you either call
        Conx.Unsketch(),
        Conx.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the connection is sketched.
            If omitted redraw is true. If you want to sketch several connections and only
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
        Unblanks the connection

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the connection

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the connection is unsketched.
            If omitted redraw is true. If you want to unsketch several connections and only
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
        Conx
            Conx object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this connection

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

