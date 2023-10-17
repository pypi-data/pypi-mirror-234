#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class report:
    fluent_name = ...
    child_names = ...
    simulation_reports = ...
    discrete_phase = ...
    fluxes = ...
    flow = ...
    modified_setting_options = ...
    population_balance = ...
    heat_exchange = ...
    system = ...
    histogram = ...
    command_names = ...

    def aero_optical_distortions(self, ):
        """
        Optics report menu.
        """

    def forces(self, options: str, domain_val: str, all_wall_zones: bool, wall_thread_list: List[str], direction_vector: List[Union[float, str]], momentum_center: List[Union[float, str]], momentum_axis: List[Union[float, str]], pressure_coordinate: str, coord_val: Union[float, str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        'forces' command.
        
        Parameters
        ----------
            options : str
                'options' child.
            domain_val : str
                'domain_val' child.
            all_wall_zones : bool
                Select all wall zones available.
            wall_thread_list : typing.List[str]
                'wall_thread_list' child.
            direction_vector : typing.List[real]
                'direction_vector' child.
            momentum_center : typing.List[real]
                'momentum_center' child.
            momentum_axis : typing.List[real]
                'momentum_axis' child.
            pressure_coordinate : str
                'pressure_coordinate' child.
            coord_val : real
                'coord_val' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def mphase_summary(self, verbosity_option: str):
        """
        Multiphase Summary and Recommendations.
        
        Parameters
        ----------
            verbosity_option : str
                'verbosity_option' child.
        
        """

    def particle_summary(self, injection_names: List[str]):
        """
        Print summary report for all current particles.
        
        Parameters
        ----------
            injection_names : typing.List[str]
                'injection_names' child.
        
        """

    def path_line_summary(self, ):
        """
        Print path-line-summary report.
        """

    def projected_surface_area(self, surface_id_val: List[int], min_feature_size: Union[float, str], proj_plane_norm_comp: List[Union[float, str]]):
        """
        Print total area of the projection of a group of surfaces to a plane.
        
        Parameters
        ----------
            surface_id_val : typing.List[int]
                'surface_id_val' child.
            min_feature_size : real
                'min_feature_size' child.
            proj_plane_norm_comp : typing.List[real]
                'proj_plane_norm_comp' child.
        
        """

    def summary(self, write_to_file: bool, file_name: str, overwrite: bool):
        """
        Print report summary.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def surface_integrals(self, report_type: str, surface_id: List[str], add_custom_vector: bool, cust_vec_name: str, domain_cx: str, cell_cx: str, domain_cy: str, cell_cy: str, domain_cz: str, cell_cz: str, cust_vec_func: str, domain_report: str, cell_report: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Create a surface integral report.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            surface_id : typing.List[str]
                'surface_id' child.
            add_custom_vector : bool
                'add_custom_vector' child.
            cust_vec_name : str
                'cust_vec_name' child.
            domain_cx : str
                'domain_cx' child.
            cell_cx : str
                'cell_cx' child.
            domain_cy : str
                'domain_cy' child.
            cell_cy : str
                'cell_cy' child.
            domain_cz : str
                'domain_cz' child.
            cell_cz : str
                'cell_cz' child.
            cust_vec_func : str
                'cust_vec_func' child.
            domain_report : str
                'domain_report' child.
            cell_report : str
                'cell_report' child.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def volume_integrals(self, report_type: str, thread_id_list: List[str], domain: str, cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            thread_id_list : typing.List[str]
                'thread_id_list' child.
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

