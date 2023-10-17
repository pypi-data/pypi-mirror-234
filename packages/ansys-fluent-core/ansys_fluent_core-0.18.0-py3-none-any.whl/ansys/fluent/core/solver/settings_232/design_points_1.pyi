#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class design_points:
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

    def duplicate(self, design_point: str):
        """
        Duplicate Design Point.
        
        Parameters
        ----------
            design_point : str
                'design_point' child.
        
        """

    def create_1(self, write_data: bool, capture_simulation_report_data: bool):
        """
        Add new Design Point.
        
        Parameters
        ----------
            write_data : bool
                'write_data' child.
            capture_simulation_report_data : bool
                'capture_simulation_report_data' child.
        
        """

    def load_case_data(self, ):
        """
        Loads relevant case/data file for current design point.
        """

    def set_as_current(self, design_point: str):
        """
        Set current design point.
        
        Parameters
        ----------
            design_point : str
                'design_point' child.
        
        """

    def delete_design_points(self, design_points: List[str]):
        """
        Delete Design Points.
        
        Parameters
        ----------
            design_points : typing.List[str]
                'design_points' child.
        
        """

    def save_journals(self, separate_journals: bool):
        """
        Save Journals.
        
        Parameters
        ----------
            separate_journals : bool
                'separate_journals' child.
        
        """

    def clear_generated_data(self, design_points: List[str]):
        """
        Clear Generated Data.
        
        Parameters
        ----------
            design_points : typing.List[str]
                'design_points' child.
        
        """

    def update_current(self, ):
        """
        Update Current Design Point.
        """

    def update_all(self, ):
        """
        Update All Design Point.
        """

    def update_selected(self, design_points: List[str]):
        """
        Update Selected Design Points.
        
        Parameters
        ----------
            design_points : typing.List[str]
                'design_points' child.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
