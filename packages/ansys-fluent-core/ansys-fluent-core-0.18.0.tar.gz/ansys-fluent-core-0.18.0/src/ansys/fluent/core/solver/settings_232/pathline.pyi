#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class pathline:
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

    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        
        """

    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
