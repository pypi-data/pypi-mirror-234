import Oasys.gRPC


# Metaclass for static properties and constants
class WorkflowType(type):
    _consts = {'UNIT_SYSTEM_NONE', 'UNIT_SYSTEM_U1', 'UNIT_SYSTEM_U2', 'UNIT_SYSTEM_U3', 'UNIT_SYSTEM_U4', 'UNIT_SYSTEM_U5', 'UNIT_SYSTEM_U6'}

    def __getattr__(cls, name):
        if name in WorkflowType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Workflow(Oasys.gRPC.OasysItem, metaclass=WorkflowType):


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
    def ModelIdFromIndex(model_index):
        """
        Returns the id of a model that has data for the selected workflow by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the id for

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "ModelIdFromIndex", model_index)

    def ModelUnitSystemFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the unit system of a model that has data for the selected workflow by index (starting at 0).
        Will be Workflow.UNIT_SYSTEM_NONE or
        Workflow.UNIT_SYSTEM_U1 or
        Workflow.UNIT_SYSTEM_U2 or
        Workflow.UNIT_SYSTEM_U3 or
        Workflow.UNIT_SYSTEM_U4 or
        Workflow.UNIT_SYSTEM_U5 or
        Workflow.UNIT_SYSTEM_U6

        Parameters
        ----------
        model_index : integer
            The index of the model to return the unit system for
        workflow_name : string
            The workflow name to return the unit system for. This is required when a PRIMER item is
            generated from REPORTER. If it is not specified the first workflow unit system associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "ModelUnitSystemFromIndex", model_index, workflow_name)

    def ModelUserDataFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the user data associated with a model that has data for the selected workflow by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the user data for
        workflow_name : string
            The workflow name to return the user data for. This is required when a PRIMER item is
            generated from REPORTER. If it is not specified the first workflow user data associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        dict
            Dict
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "ModelUserDataFromIndex", model_index, workflow_name)

    def NumberOfModels():
        """
        Returns the number of models that have data for the workflow selected by the user

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NumberOfModels")

    def Refresh():
        """
        Scan for fresh workflow data

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Refresh")

    def WorkflowDefinitionFilename(workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the workflow definition filename

        Parameters
        ----------
        workflow_name : string
            The workflow name to return the workflow defintion filename for. This is required when a PRIMER item is
            generated from REPORTER. If it is not specified the first workflow user data associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        ?
            string
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WorkflowDefinitionFilename", workflow_name)

    def WriteToFile(user_data, output_filename, workflow_definition_filename, extra=Oasys.gRPC.defaultArg):
        """
        Writes a workflow to a JSON file. If the file already exists the workflow
        is added to the file (or updated if it is already in the file)

        Parameters
        ----------
        user_data : object
            Object containing user data required for the workflow
        output_filename : string
            Filename to write to
        workflow_definition_filename : string
            Filename of the workflow definition file
        extra : dict
            Extra workflow information

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WriteToFile", user_data, output_filename, workflow_definition_filename, extra)

    def WriteToModel(user_data, model, workflow_definition_filename, extra=Oasys.gRPC.defaultArg):
        """
        Writes a workflow to a model (updating it if it already exists)

        Parameters
        ----------
        user_data : object
            Object containing user data required for the workflow
        model : Model
            Model to write to
        workflow_definition_filename : string
            Filename of the workflow definition file
        extra : dict
            Extra workflow information

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WriteToModel", user_data, model, workflow_definition_filename, extra)

