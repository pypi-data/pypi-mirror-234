import Oasys.gRPC


# Metaclass for static properties and constants
class HistoryType(type):
    _consts = {'ACOUSTIC', 'ALL_TYPES', 'BEAM', 'BEAM_SET', 'DISCRETE', 'DISCRETE_SET', 'NODE', 'NODE_SET', 'SEATBELT', 'SHELL', 'SHELL_SET', 'SOLID', 'SOLID_SET', 'SPH', 'SPH_SET', 'TSHELL', 'TSHELL_SET'}

    def __getattr__(cls, name):
        if name in HistoryType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class History(Oasys.gRPC.OasysItem, metaclass=HistoryType):
    _props = {'cid', 'exists', 'heading', 'hfo', 'id', 'include', 'local', 'model', 'ref'}
    _rprops = {'type'}


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in History._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in History._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in History._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in History._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, id, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, id, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the database histories in the model

        Parameters
        ----------
        model : Model
            Model that all database histories will be blanked in
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, type, redraw)

    def BlankFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged database histories in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged database histories will be blanked in
        flag : Flag
            Flag set on the database histories that you want to blank
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankFlagged", model, flag, type, redraw)

    def Create(model, type, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a database history

        Parameters
        ----------
        model : Model
            Model that the database history will be created in
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET
        modal : boolean
            If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        History
            History object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, type, modal)

    def First(model, type=Oasys.gRPC.defaultArg):
        """
        Returns the first database history in the model

        Parameters
        ----------
        model : Model
            Model to get first database history in
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types

        Returns
        -------
        History
            History object (or None if there are no database histories in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model, type)

    def FlagAll(model, flag, type=Oasys.gRPC.defaultArg):
        """
        Flags all of the database histories in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all database histories will be flagged in
        flag : Flag
            Flag to set on the database histories
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag, type)

    def GetAll(model, type=Oasys.gRPC.defaultArg):
        """
        Returns an array of History objects for all of the database histories in a models in Primer

        Parameters
        ----------
        model : Model
            Model to get database histories from
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types

        Returns
        -------
        list
            List of History objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll", model, type)

    def GetFromID(model, database_history_number):
        """
        Returns the History object for a database history ID

        Parameters
        ----------
        model : Model
            Model to find the database history in
        database_history_number : integer
            number of the database history you want the History object for

        Returns
        -------
        History
            History object (or None if database history does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, database_history_number)

    def Last(model, type=Oasys.gRPC.defaultArg):
        """
        Returns the last database history in the model

        Parameters
        ----------
        model : Model
            Model to get last database history in
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types

        Returns
        -------
        History
            History object (or None if there are no database histories in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model, type)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a database history

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only database histories from that model can be picked.
            If the argument is a Flag then only database histories that
            are flagged with limit can be selected.
            If omitted, or null, any database histories from any model can be selected.
            from any model
        modal : boolean
            If picking is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the pick will be modal

        Returns
        -------
        History
            History object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select database histories using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting database histories
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            If the argument is a Model then only database histories from that model can be selected.
            If the argument is a Flag then only database histories that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or null, any database histories from any model can be selected
        modal : boolean
            If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of items selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged database histories in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged database histories will be sketched in
        flag : Flag
            Flag set on the database histories that you want to sketch
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types
        redraw : boolean
            If model should be redrawn or not.
            If omitted redraw is true. If you want to do several (un)sketches and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SketchFlagged", model, flag, type, redraw)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg, type=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the database histories in the model

        Parameters
        ----------
        model : Model
            Model that all database histories will be unblanked in
        redraw : boolean
            If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll", model, redraw, type)

    def UnblankFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged database histories in the model

        Parameters
        ----------
        model : Model
            Model that the flagged database histories will be unblanked in
        flag : Flag
            Flag set on the database histories that you want to unblank
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankFlagged", model, flag, type, redraw)

    def UnflagAll(model, flag, type=Oasys.gRPC.defaultArg):
        """
        Unsets a defined flag on all of the database histories in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all database histories will be unset in
        flag : Flag
            Flag to unset on the database histories
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag, type)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all database histories

        Parameters
        ----------
        model : Model
            Model that all database histories will be unblanked in
        redraw : boolean
            If model should be redrawn or not after the database histories are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchAll", model, redraw)

    def UnsketchFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all flagged database histories

        Parameters
        ----------
        model : Model
            Model that all database histories will be unblanked in
        flag : Flag
            Flag set on the database histories that you want to sketch
        type : constant
            The database history type. Can be History.ACOUSTIC or
            History.BEAM or
            History.BEAM_SET or
            History.DISCRETE or
            History.DISCRETE_SET or
            History.NODE or
            History.NODE_SET or
            History.SEATBELT or
            History.SHELL or
            History.SHELL_SET or
            History.SOLID or
            History.SOLID_SET or
            History.SPH or
            History.SPH_SET or
            History.TSHELL or
            History.TSHELL_SET or
            History.ALL_TYPES.
            If omitted, applied to all database history types
        redraw : boolean
            If model should be redrawn or not after the database histories are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag, type, redraw)



# Instance methods
    def Blanked(self):
        """
        Checks if the database history is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the database history

        Parameters
        ----------
        flag : Flag
            Flag to clear on the database history

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Edit(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to edit the database history

        Parameters
        ----------
        modal : boolean
            If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Edit", modal)

    def Flagged(self, flag):
        """
        Checks if the database history is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to clear on the database history

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Keyword(self):
        """
        Returns the keyword for this database history (*DATABASE_HISTORY).
        Note that a carriage return is not added.
        See also History.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the database history.
        Note that a carriage return is not added.
        See also History.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next database history in the model

        Returns
        -------
        History
            History object (or None if there are no more database histories in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous database history in the model

        Returns
        -------
        History
            History object (or None if there are no more database histories in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the database history

        Parameters
        ----------
        flag : Flag
            Flag to set on the database history

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the database history. The database history will be sketched until you either call
        History.Unsketch(),
        History.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the database history is sketched.
            If omitted redraw is true. If you want to sketch several database histories and only
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
        Unsketches the database history

        Parameters
        ----------
        redraw : boolean
            If model should be redrawn or not after the database history is unsketched.
            If omitted redraw is true. If you want to unsketch several database histories and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def Xrefs(self):
        """
        Returns the cross references for this database history

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

