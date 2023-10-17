#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class import_:
    fluent_name = ...
    child_names = ...
    create_zones_from_ccl = ...
    command_names = ...

    def read(self, file_type: str, file_name: str):
        """
        'read' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
        
        """

    def chemkin_report_each_line(self, report_each_line: bool):
        """
        'chemkin_report_each_line' command.
        
        Parameters
        ----------
            report_each_line : bool
                Enable/disable reporting after reading each line.
        
        """

    def import_fmu(self, file_name: str):
        """
        Import a FMU file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

