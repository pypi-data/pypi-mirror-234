#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
class ensight(Command):
    """
    Write EnSight 6 geometry, velocity, and scalar files.
    
    Parameters
    ----------
        name : str
            'name' child.
        cell_func_domain_export : typing.List[str]
            'cell_func_domain_export' child.
    
    """

    fluent_name = "ensight"

    argument_names = \
        ['name', 'cell_func_domain_export']

    name: name_cls = name_cls
    """
    name argument of ensight.
    """
    cell_func_domain_export: cell_func_domain_export_cls = cell_func_domain_export_cls
    """
    cell_func_domain_export argument of ensight.
    """
