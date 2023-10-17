import os
import subprocess
import time
import Oasys.gRPC


_connection = None
_debug      = False


def start(abspath, args=None, port=50051, memory=25, license=None, debug=False):
    if debug:
        print("Starting {}, listening on port {}".format(abspath, port))

    environ = os.environ.copy()
    if license:
        environ[ARUP_LICENSE_PATH] = license

    subprocess.Popen( [abspath, "-grpc={}".format(port)], env=environ)

# Sleep to give time for PRIMER to start
    time.sleep(5)

    return connect(port, memory, 'localhost', debug)


def connect(port=50051, memory=25, hostname='localhost', debug=False):
    if debug:
        print("Called connect with port {} and memory {}".format(port, memory))

    Oasys.PRIMER._debug      = debug
    Oasys.PRIMER._connection = Oasys.gRPC.Connection("PRIMER", port, memory, hostname, debug)
    return Oasys.PRIMER._connection


def disconnect(connection):
    if Oasys.PRIMER._debug:
        print("Called disconnect")

    connection.finalise()
    Oasys.PRIMER._connection = None


def terminate(connection):
    if Oasys.PRIMER._debug:
        print("Called terminate")

    connection.terminate()
    Oasys.PRIMER._connection = None


def createInstance(t, h):
# Classes in PRIMER
    if t == "Accelerometer":
        instance = object.__new__(Oasys.PRIMER.Accelerometer)
    elif t == "Airbag":
        instance = object.__new__(Oasys.PRIMER.Airbag)
    elif t == "Attached":
        instance = object.__new__(Oasys.PRIMER.Attached)
    elif t == "AxialForceBeam":
        instance = object.__new__(Oasys.PRIMER.AxialForceBeam)
    elif t == "Beam":
        instance = object.__new__(Oasys.PRIMER.Beam)
    elif t == "Belt":
        instance = object.__new__(Oasys.PRIMER.Belt)
    elif t == "Box":
        instance = object.__new__(Oasys.PRIMER.Box)
    elif t == "Colour":
        instance = object.__new__(Oasys.PRIMER.Colour)
    elif t == "Comment":
        instance = object.__new__(Oasys.PRIMER.Comment)
    elif t == "ConnectionProperties":
        instance = object.__new__(Oasys.PRIMER.ConnectionProperties)
    elif t == "ConstructionStages":
        instance = object.__new__(Oasys.PRIMER.ConstructionStages)
    elif t == "Contact":
        instance = object.__new__(Oasys.PRIMER.Contact)
    elif t == "ContactGuidedCable":
        instance = object.__new__(Oasys.PRIMER.ContactGuidedCable)
    elif t == "Conx":
        instance = object.__new__(Oasys.PRIMER.Conx)
    elif t == "CoordinateSystem":
        instance = object.__new__(Oasys.PRIMER.CoordinateSystem)
    elif t == "CrossSection":
        instance = object.__new__(Oasys.PRIMER.CrossSection)
    elif t == "Curve":
        instance = object.__new__(Oasys.PRIMER.Curve)
    elif t == "DeformableToRigid":
        instance = object.__new__(Oasys.PRIMER.DeformableToRigid)
    elif t == "Discrete":
        instance = object.__new__(Oasys.PRIMER.Discrete)
    elif t == "DiscreteSphere":
        instance = object.__new__(Oasys.PRIMER.DiscreteSphere)
    elif t == "Dummy":
        instance = object.__new__(Oasys.PRIMER.Dummy)
    elif t == "ElementDeath":
        instance = object.__new__(Oasys.PRIMER.ElementDeath)
    elif t == "ExtraNodes":
        instance = object.__new__(Oasys.PRIMER.ExtraNodes)
    elif t == "FreqFRF":
        instance = object.__new__(Oasys.PRIMER.FreqFRF)
    elif t == "FreqSSD":
        instance = object.__new__(Oasys.PRIMER.FreqSSD)
    elif t == "GeneralizedWeld":
        instance = object.__new__(Oasys.PRIMER.GeneralizedWeld)
    elif t == "GeometrySurface":
        instance = object.__new__(Oasys.PRIMER.GeometrySurface)
    elif t == "Group":
        instance = object.__new__(Oasys.PRIMER.Group)
    elif t == "HexSpotweldAssembly":
        instance = object.__new__(Oasys.PRIMER.HexSpotweldAssembly)
    elif t == "History":
        instance = object.__new__(Oasys.PRIMER.History)
    elif t == "Hourglass":
        instance = object.__new__(Oasys.PRIMER.Hourglass)
    elif t == "Image":
        instance = object.__new__(Oasys.PRIMER.Image)
    elif t == "Include":
        instance = object.__new__(Oasys.PRIMER.Include)
    elif t == "IntegrationBeam":
        instance = object.__new__(Oasys.PRIMER.IntegrationBeam)
    elif t == "IntegrationShell":
        instance = object.__new__(Oasys.PRIMER.IntegrationShell)
    elif t == "InterfaceComponent":
        instance = object.__new__(Oasys.PRIMER.InterfaceComponent)
    elif t == "InterfaceLinkingEdge":
        instance = object.__new__(Oasys.PRIMER.InterfaceLinkingEdge)
    elif t == "InterfaceSpringback":
        instance = object.__new__(Oasys.PRIMER.InterfaceSpringback)
    elif t == "Interpolation":
        instance = object.__new__(Oasys.PRIMER.Interpolation)
    elif t == "InterpolationSpotweld":
        instance = object.__new__(Oasys.PRIMER.InterpolationSpotweld)
    elif t == "Joint":
        instance = object.__new__(Oasys.PRIMER.Joint)
    elif t == "JointStiffness":
        instance = object.__new__(Oasys.PRIMER.JointStiffness)
    elif t == "Linear":
        instance = object.__new__(Oasys.PRIMER.Linear)
    elif t == "LoadBeam":
        instance = object.__new__(Oasys.PRIMER.LoadBeam)
    elif t == "LoadBodyGeneralized":
        instance = object.__new__(Oasys.PRIMER.LoadBodyGeneralized)
    elif t == "LoadGravity":
        instance = object.__new__(Oasys.PRIMER.LoadGravity)
    elif t == "LoadNode":
        instance = object.__new__(Oasys.PRIMER.LoadNode)
    elif t == "LoadRemovePart":
        instance = object.__new__(Oasys.PRIMER.LoadRemovePart)
    elif t == "LoadRigidBody":
        instance = object.__new__(Oasys.PRIMER.LoadRigidBody)
    elif t == "LoadShell":
        instance = object.__new__(Oasys.PRIMER.LoadShell)
    elif t == "Mass":
        instance = object.__new__(Oasys.PRIMER.Mass)
    elif t == "MassPart":
        instance = object.__new__(Oasys.PRIMER.MassPart)
    elif t == "Material":
        instance = object.__new__(Oasys.PRIMER.Material)
    elif t == "Mechanism":
        instance = object.__new__(Oasys.PRIMER.Mechanism)
    elif t == "Model":
        instance = object.__new__(Oasys.PRIMER.Model)
    elif t == "MorphBox":
        instance = object.__new__(Oasys.PRIMER.MorphBox)
    elif t == "MorphFlow":
        instance = object.__new__(Oasys.PRIMER.MorphFlow)
    elif t == "MorphPoint":
        instance = object.__new__(Oasys.PRIMER.MorphPoint)
    elif t == "NodalForceGroup":
        instance = object.__new__(Oasys.PRIMER.NodalForceGroup)
    elif t == "NodalRigidBody":
        instance = object.__new__(Oasys.PRIMER.NodalRigidBody)
    elif t == "Node":
        instance = object.__new__(Oasys.PRIMER.Node)
    elif t == "NodeSet":
        instance = object.__new__(Oasys.PRIMER.NodeSet)
    elif t == "Options":
        instance = object.__new__(Oasys.PRIMER.Options)
    elif t == "Parameter":
        instance = object.__new__(Oasys.PRIMER.Parameter)
    elif t == "Part":
        instance = object.__new__(Oasys.PRIMER.Part)
    elif t == "PrescribedAccelerometerRigid":
        instance = object.__new__(Oasys.PRIMER.PrescribedAccelerometerRigid)
    elif t == "PrescribedFinalGeometry":
        instance = object.__new__(Oasys.PRIMER.PrescribedFinalGeometry)
    elif t == "PrescribedMotion":
        instance = object.__new__(Oasys.PRIMER.PrescribedMotion)
    elif t == "PrescribedOrientationRigid":
        instance = object.__new__(Oasys.PRIMER.PrescribedOrientationRigid)
    elif t == "Pretensioner":
        instance = object.__new__(Oasys.PRIMER.Pretensioner)
    elif t == "ReferenceGeometry":
        instance = object.__new__(Oasys.PRIMER.ReferenceGeometry)
    elif t == "Retractor":
        instance = object.__new__(Oasys.PRIMER.Retractor)
    elif t == "RigidBodies":
        instance = object.__new__(Oasys.PRIMER.RigidBodies)
    elif t == "Rigidwall":
        instance = object.__new__(Oasys.PRIMER.Rigidwall)
    elif t == "Seatbelt1D":
        instance = object.__new__(Oasys.PRIMER.Seatbelt1D)
    elif t == "Seatbelt2D":
        instance = object.__new__(Oasys.PRIMER.Seatbelt2D)
    elif t == "Section":
        instance = object.__new__(Oasys.PRIMER.Section)
    elif t == "Sensor":
        instance = object.__new__(Oasys.PRIMER.Sensor)
    elif t == "SensorControl":
        instance = object.__new__(Oasys.PRIMER.SensorControl)
    elif t == "SensorDefine":
        instance = object.__new__(Oasys.PRIMER.SensorDefine)
    elif t == "SensorSwitch":
        instance = object.__new__(Oasys.PRIMER.SensorSwitch)
    elif t == "Set":
        instance = object.__new__(Oasys.PRIMER.Set)
    elif t == "Shell":
        instance = object.__new__(Oasys.PRIMER.Shell)
    elif t == "ShellReferenceGeometry":
        instance = object.__new__(Oasys.PRIMER.ShellReferenceGeometry)
    elif t == "Slipring":
        instance = object.__new__(Oasys.PRIMER.Slipring)
    elif t == "Solid":
        instance = object.__new__(Oasys.PRIMER.Solid)
    elif t == "Spc":
        instance = object.__new__(Oasys.PRIMER.Spc)
    elif t == "Sph":
        instance = object.__new__(Oasys.PRIMER.Sph)
    elif t == "Spotweld":
        instance = object.__new__(Oasys.PRIMER.Spotweld)
    elif t == "Spr2":
        instance = object.__new__(Oasys.PRIMER.Spr2)
    elif t == "StagedConstructionPart":
        instance = object.__new__(Oasys.PRIMER.StagedConstructionPart)
    elif t == "StrainShell":
        instance = object.__new__(Oasys.PRIMER.StrainShell)
    elif t == "StrainSolid":
        instance = object.__new__(Oasys.PRIMER.StrainSolid)
    elif t == "StressBeam":
        instance = object.__new__(Oasys.PRIMER.StressBeam)
    elif t == "StressSection":
        instance = object.__new__(Oasys.PRIMER.StressSection)
    elif t == "StressShell":
        instance = object.__new__(Oasys.PRIMER.StressShell)
    elif t == "StressSolid":
        instance = object.__new__(Oasys.PRIMER.StressSolid)
    elif t == "Termination":
        instance = object.__new__(Oasys.PRIMER.Termination)
    elif t == "TieBreak":
        instance = object.__new__(Oasys.PRIMER.TieBreak)
    elif t == "Transformation":
        instance = object.__new__(Oasys.PRIMER.Transformation)
    elif t == "Tshell":
        instance = object.__new__(Oasys.PRIMER.Tshell)
    elif t == "Utils":
        instance = object.__new__(Oasys.PRIMER.Utils)
    elif t == "Vector":
        instance = object.__new__(Oasys.PRIMER.Vector)
    elif t == "Velocity":
        instance = object.__new__(Oasys.PRIMER.Velocity)
    elif t == "VelocityGeneration":
        instance = object.__new__(Oasys.PRIMER.VelocityGeneration)
    elif t == "View":
        instance = object.__new__(Oasys.PRIMER.View)
    elif t == "Workflow":
        instance = object.__new__(Oasys.PRIMER.Workflow)
    elif t == "Xrefs":
        instance = object.__new__(Oasys.PRIMER.Xrefs)

# Generic object
    elif t == "ItemObject":
        instance = object.__new__(Oasys.PRIMER.ItemObject)

# Unsupported
    else:
        raise NotImplementedError("Instance type '{}' not implemented".format(t))

    instance.__dict__['_handle']  = h;
    instance.__dict__['_objtype'] = t;

    return instance
