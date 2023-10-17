#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
class tecplot(Command):
    """
    Write a Tecplot+3DV format file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surfaces : typing.List[str]
            'surfaces' child.
        cell_func_domain_export : typing.List[str]
            'cell_func_domain_export' child.
    
    """

    fluent_name = "tecplot"

    argument_names = \
        ['name', 'surfaces', 'cell_func_domain_export']

    name: name_cls = name_cls
    """
    name argument of tecplot.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces argument of tecplot.
    """
    cell_func_domain_export: cell_func_domain_export_cls = cell_func_domain_export_cls
    """
    cell_func_domain_export argument of tecplot.
    """
