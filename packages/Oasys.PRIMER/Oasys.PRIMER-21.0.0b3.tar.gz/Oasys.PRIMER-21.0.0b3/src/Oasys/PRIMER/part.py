import Oasys.gRPC


# Metaclass for static properties and constants
class PartType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Part(Oasys.gRPC.OasysItem, metaclass=PartType):
    _props = {'adpopt', 'ansid', 'attachment_nodes', 'averaged', 'cadname', 'cid', 'cmsn', 'colour', 'composite', 'composite_long', 'contact', 'dc', 'element_type', 'elform', 'eosid', 'exists', 'fd', 'fs', 'grav', 'heading', 'hgid', 'hmname', 'iga_shell', 'include', 'inertia', 'ircs', 'irl', 'ixx', 'ixy', 'ixz', 'iyy', 'iyz', 'izz', 'label', 'marea', 'mdep', 'mid', 'movopt', 'nip', 'nloc', 'nodeid', 'optt', 'pid', 'prbf', 'print', 'reposition', 'rigid', 'secid', 'sft', 'shrf', 'ssf', 'thshel', 'tm', 'tmid', 'transparency', 'tshear', 'tshell', 'vc', 'vrx', 'vry', 'vrz', 'vtx', 'vty', 'vtz', 'xc', 'xl', 'xlip', 'yc', 'yl', 'ylip', 'zc', 'zl', 'zlip'}
    _rprops = {'model'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Part._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Part._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Part._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Part._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, pid, secid, mid, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, pid, secid, mid, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def AllTableProperties(model):
        """
        Returns all of the properties available in the part table for the parts.
        The table values are returned in an array of objects (an object for each part).
        The object property names are the same as the table headers but spaces
        are replaced with underscore characters and characters other than 0-9, a-z and A-Z are removed to ensure that the
        property name is valid in JavaScript. If a table value is undefined the property value will be the JavaScript undefined
        value. If the table value is a valid number it will be a number, otherwise the value will returned as a string

        Parameters
        ----------
        model : Model
            Model that the flagged parts are in

        Returns
        -------
        list
            List of objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AllTableProperties", model)

    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that all parts will be blanked in
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
        Blanks all of the flagged parts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged parts will be blanked in
        flag : Flag
            Flag set on the parts that you want to blank
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

    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a part

        Parameters
        ----------
        model : Model
            Model that the part will be created in
        modal : boolean
            If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Part
            Part object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first part in the model

        Parameters
        ----------
        model : Model
            Model to get first part in

        Returns
        -------
        Part
            Part object (or None if there are no parts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free part label in the model.
        Also see Part.LastFreeLabel(),
        Part.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free part label in
        layer : Include number
            Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Part label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the parts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all parts will be flagged in
        flag : Flag
            Flag to set on the parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def FlagVisible(model, flag):
        """
        Flags all the unblanked parts in the model

        Parameters
        ----------
        model : Model
            Model for which all unblanked parts will be flagged in
        flag : Flag
            Flag to set on the unblanked parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagVisible", model, flag)

    def FlaggedTableProperties(model, flag):
        """
        Returns all of the properties available in the part table for the flagged parts.
        The table values are returned in an array of objects (an object for each part).
        The object property names are the same as the table headers but spaces
        are replaced with underscore characters and characters other than 0-9, a-z and A-Z are removed to ensure that the
        property name is valid in JavaScript. If a table value is undefined the property value will be the JavaScript undefined
        value. If the table value is a valid number it will be a number, otherwise the value will returned as a string

        Parameters
        ----------
        model : Model
            Model that the flagged parts are in
        flag : Flag
            Flag set on the parts that you want properties for

        Returns
        -------
        list
            List of objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlaggedTableProperties", model, flag)

    def GetAll(model):
        """
        Returns an array of Part objects for all of the parts in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get parts from

        Returns
        -------
        list
            List of Part objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Returns an array of Part objects for all of the flagged parts in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get parts from
        flag : Flag
            Flag set on the parts that you want to retrieve

        Returns
        -------
        list
            List of Part objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, number):
        """
        Returns the Part object for a part ID

        Parameters
        ----------
        model : Model
            Model to find the part in
        number : integer
            number of the part you want the Part object for

        Returns
        -------
        Part
            Part object (or None if part does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last part in the model

        Parameters
        ----------
        model : Model
            Model to get last part in

        Returns
        -------
        Part
            Part object (or None if there are no parts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free part label in the model.
        Also see Part.FirstFreeLabel(),
        Part.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free part label in
        layer : Include number
            Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Part label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def MeasurePartToPart(part1, part2):
        """
        This static method measures the distance between 
        two part objects contained in the same model or in two different models

        Parameters
        ----------
        part1 : Part
            Part to measure from
        part2 : Part
            Part to measure to

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "MeasurePartToPart", part1, part2)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) part label in the model.
        Also see Part.FirstFreeLabel(),
        Part.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free part label in
        layer : Include number
            Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Part label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a part

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only parts from that model can be picked.
            If the argument is a Flag then only parts that
            are flagged with limit can be selected.
            If omitted, or null, any parts from any model can be selected.
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
        Part
            Part object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that all parts will be renumbered in
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
        Renumbers all of the flagged parts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged parts will be renumbered in
        flag : Flag
            Flag set on the parts that you want to renumber
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
        Allows the user to select parts using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting parts
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only parts from that model can be selected.
            If the argument is a Flag then only parts that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any parts can be selected.
            from any model
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of parts selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged parts in the model. The parts will be sketched until you either call
        Part.Unsketch(),
        Part.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged parts will be sketched in
        flag : Flag
            Flag set on the parts that you want to sketch
        redraw : boolean
            If model should be redrawn or not after the parts are sketched.
            If omitted redraw is true. If you want to sketch flagged parts several times and only
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
        Returns the total number of parts in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            true if only existing parts should be counted. If false or omitted
            referenced but undefined parts will also be included in the total

        Returns
        -------
        int
            number of parts
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that all parts will be unblanked in
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
        Unblanks all of the flagged parts in the model

        Parameters
        ----------
        model : Model
            Model that the flagged parts will be unblanked in
        flag : Flag
            Flag set on the parts that you want to unblank
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
        Unsets a defined flag on all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all parts will be unset in
        flag : Flag
            Flag to unset on the parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all parts

        Parameters
        ----------
        model : Model
            Model that all parts will be unblanked in
        redraw : boolean
            If model should be redrawn or not after the parts are unsketched.
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
        Unsketches all flagged parts in the model

        Parameters
        ----------
        model : Model
            Model that all parts will be unsketched in
        flag : Flag
            Flag set on the parts that you want to unsketch
        redraw : boolean
            If model should be redrawn or not after the parts are unsketched.
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
        Associates a comment with a part

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the part is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

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

    def CentreOfGravity(self, options=Oasys.gRPC.defaultArg):
        """
        Returns the centre of gravity for a part

        Parameters
        ----------
        options : dict
            Options specifying how the mass calculation should be done

        Returns
        -------
        list
            A list containing the x, y and z coordinates for the CofG
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "CentreOfGravity", options)

    def ClearFlag(self, flag):
        """
        Clears a flag on the part

        Parameters
        ----------
        flag : Flag
            Flag to clear on the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def ClosestNode(self, x, y, z):
        """
        Finds the Node on the part closest to a coordinate

        Parameters
        ----------
        x : float
            X coordinate of point
        y : float
            Y coordinate of point
        z : float
            Z coordinate of point

        Returns
        -------
        int
            ID of Node or None if part has no nodes
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClosestNode", x, y, z)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the part. The target include of the copied part can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Part
            Part object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a part

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the part

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

    def ExtractColour(self):
        """
        Extracts the actual colour used for part.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the part colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the part

        Returns
        -------
        ?
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the part is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the part

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a part

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetCompositeData(self, ipt):
        """
        Returns the composite data for an integration point in *PART_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want the data for. Note that integration points start at 0, not 1

        Returns
        -------
        list
            A list containing the material id, thickness, beta angle and thermal material values.
            If the _COMPOSITE_LONG option is set, then the array returned will also contain the ply ID
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCompositeData", ipt)

    def GetParameter(self, prop):
        """
        Checks if a Part property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Part.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            part property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this part (*PART, *PART_SCALAR or *PART_SCALAR_VALUE).
        Note that a carriage return is not added.
        See also Part.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the part.
        Note that a carriage return is not added.
        See also Part.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Mass(self):
        """
        Returns the mass properties for a part

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Mass")

    def MaxMin(self):
        """
        Returns the max and min boundas of a part

        Returns
        -------
        list
            A list containing the xMin, xMax, yMin, yMax, zMin and zMax coordinates for a box bounding the part
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "MaxMin")

    def Next(self):
        """
        Returns the next part in the model

        Returns
        -------
        Part
            Part object (or None if there are no more parts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous part in the model

        Returns
        -------
        Part
            Part object (or None if there are no more parts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveCompositeData(self, ipt):
        """
        Removes the composite data for an integration point in *PART_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want to remove.
            Note that integration points start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveCompositeData", ipt)

    def SetCompositeData(self, ipt, mid, thick, beta, tmid, plyid=Oasys.gRPC.defaultArg, shrfac=Oasys.gRPC.defaultArg):
        """
        Sets the composite data for an integration point in *PART_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want to set the data for.
            Note that integration points start at 0, not 1
        mid : integer
            Material ID for the integration point
        thick : real
            Thickness of the integration point
        beta : real
            Material angle of the integration point
        tmid : integer
            Thermal material ID for the integration point
        plyid : integer
            Ply ID for the integration point. This should be used if the _COMPOSITE_LONG option is set for the part
        shrfac : real
            Transverse shear stress scale factor

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCompositeData", ipt, mid, thick, beta, tmid, plyid, shrfac)

    def SetFlag(self, flag):
        """
        Sets a flag on the part

        Parameters
        ----------
        flag : Flag
            Flag to set on the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the part. The part will be sketched until you either call
        Part.Unsketch(),
        Part.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the part is sketched.
            If omitted redraw is true. If you want to sketch several parts and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def TableProperties(self):
        """
        Returns all of the properties available for the part in the part table.
        The table values are returned in an object. The object property names are the same as the table headers but spaces
        are replaced with underscore characters and characters other than 0-9, a-z and A-Z are removed to ensure that the
        property name is valid in JavaScript. If a table value is undefined the property value will be the JavaScript undefined
        value. If the table value is a valid number it will be a number, otherwise the value will returned as a string

        Returns
        -------
        dict
            Dict
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "TableProperties")

    def Unblank(self):
        """
        Unblanks the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the part

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the part is unsketched.
            If omitted redraw is true. If you want to unsketch several parts and only
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
        Part
            Part object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this part

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

