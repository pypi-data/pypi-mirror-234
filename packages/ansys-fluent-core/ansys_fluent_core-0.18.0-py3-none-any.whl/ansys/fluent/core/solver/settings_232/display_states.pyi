#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class display_states:
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    def list_properties(self, object_name: str):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : str
                'to' child.
        
        """

    def use_active(self, state_name: str):
        """
        'use_active' command.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def restore_state(self, state_name: str):
        """
        Apply a display state to the active window.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def copy(self, state_name: str):
        """
        Create a new display state with settings copied from an existing display state.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def read(self, file_name: str):
        """
        Read display states from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write(self, file_name: str, state_name: List[str]):
        """
        Write display states to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            state_name : typing.List[str]
                'state_name' child.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
