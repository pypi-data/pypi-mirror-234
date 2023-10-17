#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .binary_format import binary_format as binary_format_cls
from .cellzones import cellzones as cellzones_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls
class ensight_gold_parallel_volume(Command):
    """
    Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
    
    Parameters
    ----------
        name : str
            'name' child.
        binary_format : bool
            'binary_format' child.
        cellzones : typing.List[str]
            'cellzones' child.
        cell_centered : bool
            'cell_centered' child.
        cell_function : typing.List[str]
            'cell_function' child.
    
    """

    fluent_name = "ensight-gold-parallel-volume"

    argument_names = \
        ['name', 'binary_format', 'cellzones', 'cell_centered',
         'cell_function']

    name: name_cls = name_cls
    """
    name argument of ensight_gold_parallel_volume.
    """
    binary_format: binary_format_cls = binary_format_cls
    """
    binary_format argument of ensight_gold_parallel_volume.
    """
    cellzones: cellzones_cls = cellzones_cls
    """
    cellzones argument of ensight_gold_parallel_volume.
    """
    cell_centered: cell_centered_cls = cell_centered_cls
    """
    cell_centered argument of ensight_gold_parallel_volume.
    """
    cell_function: cell_function_cls = cell_function_cls
    """
    cell_function argument of ensight_gold_parallel_volume.
    """
