#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .cell_zone_list import cell_zone_list as cell_zone_list_cls
class activate_cell_zone(Command):
    """
    'activate_cell_zone' command.
    
    Parameters
    ----------
        cell_zone_list : typing.List[str]
            'cell_zone_list' child.
    
    """

    fluent_name = "activate-cell-zone"

    argument_names = \
        ['cell_zone_list']

    cell_zone_list: cell_zone_list_cls = cell_zone_list_cls
    """
    cell_zone_list argument of activate_cell_zone.
    """
