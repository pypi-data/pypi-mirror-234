#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .zone_name import zone_name as zone_name_cls
class use_inlet_temperature_for_operating_density(Command):
    """
    Use Inlet Temperature to calculate Opearating Density.
    
    Parameters
    ----------
        zone_name : str
            'zone_name' child.
    
    """

    fluent_name = "use-inlet-temperature-for-operating-density"

    argument_names = \
        ['zone_name']

    zone_name: zone_name_cls = zone_name_cls
    """
    zone_name argument of use_inlet_temperature_for_operating_density.
    """
