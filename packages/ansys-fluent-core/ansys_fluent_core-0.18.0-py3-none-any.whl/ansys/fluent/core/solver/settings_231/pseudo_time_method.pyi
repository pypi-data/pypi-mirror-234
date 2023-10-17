#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class pseudo_time_method:
    fluent_name = ...
    child_names = ...
    formulation = ...
    relaxation_method = ...
    convergence_acceleration_for_stretched_meshes = ...
    command_names = ...

    def relaxation_bounds(self, relaxation_bounding_method: str, default_min_max_relaxation_limits: bool, minimum_allowed_effctive_relaxation: Union[float, str], maximum_allowed_effctive_relaxation: Union[float, str]):
        """
        Select relaxation bounding scheme for pseudo time method.
        
        Parameters
        ----------
            relaxation_bounding_method : str
                'relaxation_bounding_method' child.
            default_min_max_relaxation_limits : bool
                'default_min_max_relaxation_limits' child.
            minimum_allowed_effctive_relaxation : real
                'minimum_allowed_effctive_relaxation' child.
            maximum_allowed_effctive_relaxation : real
                'maximum_allowed_effctive_relaxation' child.
        
        """

