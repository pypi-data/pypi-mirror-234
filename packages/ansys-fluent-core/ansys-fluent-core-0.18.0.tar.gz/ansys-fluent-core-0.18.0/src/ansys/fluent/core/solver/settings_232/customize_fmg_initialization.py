#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .multi_level_grid import multi_level_grid as multi_level_grid_cls
from .residual_reduction_level import residual_reduction_level as residual_reduction_level_cls
from .cycle_count import cycle_count as cycle_count_cls
class customize_fmg_initialization(Command):
    """
    'customize_fmg_initialization' command.
    
    Parameters
    ----------
        multi_level_grid : int
            'multi_level_grid' child.
        residual_reduction_level : typing.List[real]
            'residual_reduction_level' child.
        cycle_count : typing.List[real]
            'cycle_count' child.
    
    """

    fluent_name = "customize-fmg-initialization"

    argument_names = \
        ['multi_level_grid', 'residual_reduction_level', 'cycle_count']

    multi_level_grid: multi_level_grid_cls = multi_level_grid_cls
    """
    multi_level_grid argument of customize_fmg_initialization.
    """
    residual_reduction_level: residual_reduction_level_cls = residual_reduction_level_cls
    """
    residual_reduction_level argument of customize_fmg_initialization.
    """
    cycle_count: cycle_count_cls = cycle_count_cls
    """
    cycle_count argument of customize_fmg_initialization.
    """
