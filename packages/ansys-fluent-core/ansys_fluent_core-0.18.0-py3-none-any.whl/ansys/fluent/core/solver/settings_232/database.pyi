#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class database:
    fluent_name = ...
    child_names = ...
    database_type = ...
    command_names = ...

    def copy_by_formula(self, type: str, formula: str):
        """
        Copy a material from the database (pick by formula).
        
        Parameters
        ----------
            type : str
                'type' child.
            formula : str
                'formula' child.
        
        """

    def copy_by_name(self, type: str, name: str):
        """
        Copy a material from the database (pick by name).
        
        Parameters
        ----------
            type : str
                'type' child.
            name : str
                'name' child.
        
        """

    def list_materials(self, ):
        """
        List all materials in the database.
        """

    def list_properties(self, name: str):
        """
        List the properties of a material in the database.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

