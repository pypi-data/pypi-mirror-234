#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class operating_conditions:
    fluent_name = ...
    child_names = ...
    gravity = ...
    real_gas_state = ...
    operating_pressure = ...
    reference_pressure_location = ...
    reference_pressure_method = ...
    operating_density = ...
    operating_temperature = ...
    command_names = ...

    def used_ref_pressure_location(self, ):
        """
        See the actual coordinates of reference pressure used.
        """

    def use_inlet_temperature_for_operating_density(self, zone_name: str):
        """
        Use Inlet Temperature to calculate Opearating Density.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
        
        """

