#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .wall_function import wall_function as wall_function_cls
from .surface_name_list import surface_name_list as surface_name_list_cls
class custom_heat_flux(Command):
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

    fluent_name = "custom-heat-flux"

    argument_names = \
        ['name', 'wall_function', 'surface_name_list']

    name: name_cls = name_cls
    """
    name argument of custom_heat_flux.
    """
    wall_function: wall_function_cls = wall_function_cls
    """
    wall_function argument of custom_heat_flux.
    """
    surface_name_list: surface_name_list_cls = surface_name_list_cls
    """
    surface_name_list argument of custom_heat_flux.
    """
