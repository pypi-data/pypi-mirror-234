#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class export:
    fluent_name = ...
    child_names = ...
    sc_def_file_settings = ...
    settings = ...
    command_names = ...

    def abaqus(self, name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an ABAQUS file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
        
        """

    def mechanical_apdl(self, name: str, thread_name_list: List[str]):
        """
        Write an Mechanical APDL file.
        
        Parameters
        ----------
            name : str
                'name' child.
            thread_name_list : typing.List[str]
                'thread_name_list' child.
        
        """

    def mechanical_apdl_input(self, name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an Mechanical APDL Input file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
        
        """

    def custom_heat_flux(self, name: str, wall_function: bool, surface_name_list: List[str]):
        """
        Write a generic file for heat transfer.
        
        Parameters
        ----------
            name : str
                'name' child.
            wall_function : bool
                'wall_function' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
        
        """

    def icemcfd_for_icepak(self, name: str):
        """
        Write a binary ICEMCFD domain file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def fast_mesh(self, name: str):
        """
        Write a FAST/Plot3D unstructured mesh file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def fast_solution(self, name: str):
        """
        Write a FAST/Plot3D unstructured solution file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def fast_velocity(self, name: str):
        """
        Write a FAST/Plot3D unstructured vector function file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def taitherm(self, name: str, surface_name_list: List[str], wall_function: bool, htc_on_walls: bool):
        """
        Write a TAITherm file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
            wall_function : bool
                'wall_function' child.
            htc_on_walls : bool
                'htc_on_walls' child.
        
        """

