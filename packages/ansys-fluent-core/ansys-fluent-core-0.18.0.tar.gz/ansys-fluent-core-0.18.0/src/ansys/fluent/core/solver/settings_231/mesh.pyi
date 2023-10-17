#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class mesh:
    fluent_name = ...
    child_names = ...
    adapt = ...
    check_before_solve = ...
    check_verbosity = ...
    enhanced_orthogonal_quality = ...
    matching_tolerance = ...
    show_periodic_shadow_zones = ...
    reorder = ...
    repair_improve = ...
    surface_mesh = ...
    polyhedra = ...
    command_names = ...

    def adjacency(self, ):
        """
        View and rename face zones adjacent to selected cell zones.
        """

    def check(self, ):
        """
        Perform various mesh consistency checks.
        """

    def memory_usage(self, ):
        """
        Report solver memory use.
        """

    def mesh_info(self, print_level: int):
        """
        'mesh_info' command.
        
        Parameters
        ----------
            print_level : int
                Print zone information size.
        
        """

    def quality(self, ):
        """
        Perform analysis of mesh quality.
        """

    def rotate(self, angle: Union[float, str], origin: Tuple[Union[float, str], Union[float, str], Union[float, str], axis_components: Tuple[Union[float, str], Union[float, str], Union[float, str]):
        """
        Rotate the mesh.
        
        Parameters
        ----------
            angle : real
                'angle' child.
            origin : typing.Tuple[real, real, real]
                'origin' child.
            axis_components : typing.Tuple[real, real, real]
                'axis_components' child.
        
        """

    def scale(self, x_scale: Union[float, str], y_scale: Union[float, str], z_scale: Union[float, str]):
        """
        'scale' command.
        
        Parameters
        ----------
            x_scale : real
                'x_scale' child.
            y_scale : real
                'y_scale' child.
            z_scale : real
                'z_scale' child.
        
        """

    def size_info(self, ):
        """
        Print mesh size.
        """

    def redistribute_boundary_layer(self, thread_id: int, growth_rate: Union[float, str]):
        """
        Enforce growth rate in boundary layer.
        
        Parameters
        ----------
            thread_id : int
                'thread_id' child.
            growth_rate : real
                'growth_rate' child.
        
        """

    def swap_mesh_faces(self, ):
        """
        Swap mesh faces.
        """

    def smooth_mesh(self, type_of_smoothing: str, number_of_iterations: int, relaxtion_factor: Union[float, str], percentage_of_cells: Union[float, str], skewness_threshold: Union[float, str]):
        """
        Smooth the mesh using quality-based, Laplace or skewness methods.
        
        Parameters
        ----------
            type_of_smoothing : str
                'type_of_smoothing' child.
            number_of_iterations : int
                'number_of_iterations' child.
            relaxtion_factor : real
                'relaxtion_factor' child.
            percentage_of_cells : real
                'percentage_of_cells' child.
            skewness_threshold : real
                'skewness_threshold' child.
        
        """

    def replace(self, name: str, zones: bool):
        """
        Replace mesh and interpolate data.
        
        Parameters
        ----------
            name : str
                'name' child.
            zones : bool
                'zones' child.
        
        """

    def translate(self, offset: Tuple[Union[float, str], Union[float, str], Union[float, str]):
        """
        Translate the mesh.
        
        Parameters
        ----------
            offset : typing.Tuple[real, real, real]
                'offset' child.
        
        """

