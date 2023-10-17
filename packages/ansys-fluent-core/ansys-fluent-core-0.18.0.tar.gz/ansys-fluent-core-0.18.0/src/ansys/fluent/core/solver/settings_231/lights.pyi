#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class lights:
    fluent_name = ...
    child_names = ...
    headlight_setting = ...
    lights_on = ...
    lighting_interpolation = ...
    command_names = ...

    def set_ambient_color(self, rgb_vector: Tuple[Union[float, str], Union[float, str], Union[float, str]):
        """
        'set_ambient_color' command.
        
        Parameters
        ----------
            rgb_vector : typing.Tuple[real, real, real]
                'rgb_vector' child.
        
        """

    def set_light(self, light_number: int, light_on: bool, rgb_vector: Tuple[Union[float, str], Union[float, str], Union[float, str], use_view_factor: bool, change_light_direction: bool, direction_vector: Tuple[Union[float, str], Union[float, str], Union[float, str]):
        """
        'set_light' command.
        
        Parameters
        ----------
            light_number : int
                'light_number' child.
            light_on : bool
                'light_on' child.
            rgb_vector : typing.Tuple[real, real, real]
                'rgb_vector' child.
            use_view_factor : bool
                'use_view_factor' child.
            change_light_direction : bool
                'change_light_direction' child.
            direction_vector : typing.Tuple[real, real, real]
                'direction_vector' child.
        
        """

