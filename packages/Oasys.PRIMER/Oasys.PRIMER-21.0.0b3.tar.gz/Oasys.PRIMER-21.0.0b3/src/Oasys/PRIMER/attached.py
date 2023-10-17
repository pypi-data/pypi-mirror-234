import Oasys.gRPC


# Metaclass for static properties and constants
class AttachedType(type):
    _consts = {'SINGLE', 'WHOLE'}

    def __getattr__(cls, name):
        if name in AttachedType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Attached(Oasys.gRPC.OasysItem, metaclass=AttachedType):


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Beam3rdNodes(setting):
        """
        Sets the find attached option for beam 3rd nodes on or off

        Parameters
        ----------
        setting : boolean
            If true beam 3rd nodes are considered for find attached, if false, they are not

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Beam3rdNodes", setting)

    def BeamPid(setting):
        """
        Sets the find attached option for beam pid on or off

        Parameters
        ----------
        setting : boolean
            If true beam pid's are considered for find attached, if false, they are not

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BeamPid", setting)

    def Deformable(setting):
        """
        Sets the deformable option for find attached

        Parameters
        ----------
        setting : constant
            Option. Can be Attached.WHOLE,
            Attached.SINGLE

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Deformable", setting)

    def FlagPart(setting):
        """
        Sets an option to flag parts after a find attached if any elements within that part are flagged

        Parameters
        ----------
        setting : boolean
            If true, parts are flagged after a find attached if any elements within that part are flagged, if false, they are not

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagPart", setting)

    def Recursive(setting, number=Oasys.gRPC.defaultArg):
        """
        Sets the find attached option for recursive on or off

        Parameters
        ----------
        setting : boolean
            If true recursive is on, if false, it is off
        number : integer
            Option to set the number of find attached iterations used when the recursive option is set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Recursive", setting, number)

    def Rigid(setting):
        """
        Sets the rigid option for find attached

        Parameters
        ----------
        setting : constant
            Option. Can be Attached.WHOLE,
            Attached.SINGLE

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Rigid", setting)

    def SetEntity(type, setting):
        """
        Sets entity to be on or off to find attached through

        Parameters
        ----------
        type : string
            The type of the item to switch on or off (for a list of types see Appendix I of the PRIMER manual)
        setting : boolean
            If true you turn the entity switch on, if false you turn it off

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetEntity", type, setting)

    def TiedContacts(setting):
        """
        Sets the find attached option for tied contacts on or off

        Parameters
        ----------
        setting : boolean
            If true tied contacts are considered for find attached, if false, they are not

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "TiedContacts", setting)

