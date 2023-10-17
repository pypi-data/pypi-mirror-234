#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class lights:
    fluent_name = ...
    child_names = ...
    ambient_color = ...
    headlight_setting = ...
    lights_on = ...
    lighting_interpolation = ...
    command_names = ...

    def set_light(self, light_number: int, light_on: bool, rgb_vector: List[Union[float, str]], use_view_factor: bool, change_light_direction: bool, direction_vector: List[Union[float, str]]):
        """
        'set_light' command.
        
        Parameters
        ----------
            light_number : int
                'light_number' child.
            light_on : bool
                'light_on' child.
            rgb_vector : typing.List[real]
                'rgb_vector' child.
            use_view_factor : bool
                'use_view_factor' child.
            change_light_direction : bool
                'change_light_direction' child.
            direction_vector : typing.List[real]
                'direction_vector' child.
        
        """

