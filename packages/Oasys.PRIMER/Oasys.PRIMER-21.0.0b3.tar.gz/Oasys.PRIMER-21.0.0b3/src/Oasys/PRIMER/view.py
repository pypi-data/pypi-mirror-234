import Oasys.gRPC


# Metaclass for static properties and constants
class ViewType(type):
    _consts = {'ABSOLUTE', 'ADDEDMASS', 'ADDEDMASSPART', 'AREA', 'ASPECTRATIO', 'CONTOUR', 'DENSITY', 'ELEMPROPS', 'ELEMQUAL', 'EMPFINALMASS', 'EMPNSMASS', 'EMPSTRUCTMASS', 'FAILEDCRITERIA', 'FINALMASS', 'FORM', 'FORMULATION', 'INITVELRES', 'INITVELS', 'INITVELX', 'INITVELY', 'INITVELZ', 'INTPOINT', 'INTPOINTS', 'ISO', 'JACOBIAN', 'LOADSHELLDIRECTION', 'MASSSCALE', 'MATERIALNUMBER', 'MATLPROPS', 'MAXINTANGLE', 'MAXSTRAIN', 'MININTANGLE', 'MINLENGTH', 'MINSTRAIN', 'PARAMETRICCOORD', 'PARTMASS', 'PERCENTADDEDMASS', 'PERCENTADDEDMASSPART', 'PLASTICSTRAIN', 'POISSONRATIO', 'QUALIMPERF', 'REMAINING', 'SHELLNORMALS', 'SHELLTHICKNESS', 'SKEW', 'STRUCTMASS', 'TAPER', 'TETCOLLAPSE', 'THINNING', 'TIMESTEP', 'VECTOR', 'VOLUME', 'WARPAGE', 'XY', 'XZ', 'YIELDSTRESS', 'YOUNGMODULUS', 'YZ'}

    def __getattr__(cls, name):
        if name in ViewType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class View(Oasys.gRPC.OasysItem, metaclass=ViewType):


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
    def Ac():
        """
        Autoscales the view

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Ac")

    def Ct():
        """
        Does a contour plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Ct")

    def Hi():
        """
        Does a Hidden line plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Hi")

    def Li():
        """
        Does a line (wireframe) plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Li")

    def Redraw():
        """
        Redraws the plot using the current plot mode

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Redraw")

    def SetContourType(view_type, view_subtype, view_subtype2):
        """
        Sets a contour type (and subtype)

        Parameters
        ----------
        view_type : constant
            The type of contour to plot. Can be: 
            View.TIMESTEP 
            View.SHELLTHICKNESS 
            View.SHELLNORMALS 
            View.LOADSHELLDIRECTION 
            View.ELEMPROPS 
            View.ELEMQUAL 
            View.MASSSCALE 
            View.MATLPROPS 
            View.INITVELS 
            View.PARTMASS
        view_subtype : constant
            The subtype of contour to plot.
            Note: This second argument is NOT required for types TIMESTEP and LOADSHELLDIRECTION. 
            Subtypes for Type TIMESTEP: 
            No subtypes 
            Subtypes for Type SHELLTHICKNESS: 
            View.ABSOLUTE 
            View.THINNING 
            View.REMAINING 
            Subtypes for SHELLNORMALS: 
            View.CONTOUR 
            View.VECTOR 
            Subtypes for Type LOADSHELLDIRECTION: 
            No subtypes 
            Subtypes for Type ELEMPROPS: 
            View.FORMULATION 
            View.INTPOINTS 
            View.PLASTICSTRAIN 
            View.FORM 
            View.AREA 
            View.VOLUME 
            Subtypes for Type ELEMQUAL: 
            View.MINLENGTH 
            View.ASPECTRATIO 
            View.WARPAGE 
            View.SKEW 
            View.MININTANGLE 
            View.MAXINTANGLE 
            View.JACOBIAN 
            View.TAPER 
            View.TETCOLLAPSE 
            View.QUALIMPERF 
            View.FAILEDCRITERIA 
            Subtypes for Type MASSSCALE: 
            View.PERCENTADDEDMASS 
            View.ADDEDMASS 
            View.PERCENTADDEDMASSPART 
            View.ADDEDMASSPART 
            Subtypes for Type MATLPROPS: 
            View.DENSITY 
            View.YIELDSTRESS 
            View.POISSONRATIO 
            View.YOUNGMODULUS 
            View.MATERIALNUMBER 
            Subtypes for Type INITVELS: 
            View.INITVELX 
            View.INITVELY 
            View.INITVELZ 
            View.INITVELRES 
            Subtypes for Type PARTMASS: 
            View.STRUCTMASS 
            View.EMPSTRUCTMASS 
            View.EMPNSMASS 
            View.FINALMASS 
            View.EMPFINALMASS
        view_subtype2 : constant
            The subtype of contour to plot.
            Note: This third argument is required only for ELEMENTPROP ->PLASTICSTRAIN/FORM/AREA/VOLUME. 
            The default is PARAMETRIC COORDINATE. 
            Subtypes for Type ELEMENTPROP -> PLASTICSTRAIN/FORM/AREA/VOLUME: 
            View.PARAMETRICCOORD 
            View.INTEGRATIONPOINT 
            View.MINSTRAIN 
            View.MAXSTRAIN

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetContourType", view_type, view_subtype, view_subtype2)

    def Sh():
        """
        Does a shaded plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Sh")

    def Show(view_type):
        """
        Redraws using one of the standard views

        Parameters
        ----------
        view_type : constant
            The view to show. Can be +/-View.XY,
            +/-View.YZ,
            +/-View.XZ or
            +/-View.ISO

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Show", view_type)

    def Si():
        """
        Does a shaded image contour plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Si")

    def Vec():
        """
        Does a vector plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Vec")

