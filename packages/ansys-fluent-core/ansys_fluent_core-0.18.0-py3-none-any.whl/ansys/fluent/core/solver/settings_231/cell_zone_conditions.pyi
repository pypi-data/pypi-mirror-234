#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class cell_zone_conditions:
    fluent_name = ...
    child_names = ...
    fluid = ...
    solid = ...
    command_names = ...

    def change_type(self, zone_list: List[str], new_type: str):
        """
        'change_type' command.
        
        Parameters
        ----------
            zone_list : typing.List[str]
                'zone_list' child.
            new_type : str
                'new_type' child.
        
        """

    def activate_cell_zone(self, cell_zone_list: List[str]):
        """
        'activate_cell_zone' command.
        
        Parameters
        ----------
            cell_zone_list : typing.List[str]
                'cell_zone_list' child.
        
        """

    def mrf_to_sliding_mesh(self, zone_id: int):
        """
        Change motion specification from MRF to moving mesh.
        
        Parameters
        ----------
            zone_id : int
                'zone_id' child.
        
        """

    def convert_all_solid_mrf_to_solid_motion(self, ):
        """
        Change all solid zones motion specification from MRF to solid motion.
        """

    def copy_mrf_to_mesh_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def copy_mesh_to_mrf_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

