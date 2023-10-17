#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class fluxes:
    fluent_name = ...
    command_names = ...

    def mass_flow(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print mass flow rate at inlets and outlets.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def heat_transfer(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def heat_transfer_sensible(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print sensible heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def rad_heat_trans(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print radiation heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def film_mass_flow(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print film mass flow rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def film_heat_transfer(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print film heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def pressure_work(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print pressure work rate at moving boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def viscous_work(self, domain_val: str, all_bndry_zones: bool, zone_list: List[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print viscous work rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                Select all the boundary/interior zones.
            zone_list : typing.List[str]
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

