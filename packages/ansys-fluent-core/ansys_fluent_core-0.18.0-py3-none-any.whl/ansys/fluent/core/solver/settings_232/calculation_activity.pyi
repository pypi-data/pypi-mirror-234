#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class calculation_activity:
    fluent_name = ...
    child_names = ...
    execute_commands = ...
    solution_animations = ...
    poor_mesh_numerics = ...
    command_names = ...

    def enable_strategy(self, enable: bool):
        """
        Specify whether automatic initialization and case modification should be enabled.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
        
        """

    def copy_modification(self, mod_name: str):
        """
        Copy a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def delete_modification(self, mod_name: str):
        """
        Delete a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def enable_modification(self, mod_name: str):
        """
        Enable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def disable_modification(self, mod_name: str):
        """
        Disable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def import_modifications(self, filename: str):
        """
        Import a list of case modifications from a tsv file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def export_modifications(self, command_list: List[str], filename: str):
        """
        Export all case modifications to a tsv file.
        
        Parameters
        ----------
            command_list : typing.List[str]
                'command_list' child.
            filename : str
                'filename' child.
        
        """

    def continue_strategy_execution(self, ):
        """
        Continue execution of the automatic initialization and case modification strategy defined at present.
        """

