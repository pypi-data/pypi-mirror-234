#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .scope import scope as scope_cls
from .cell_zones import cell_zones as cell_zones_cls
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .format_class import format_class as format_class_cls
from .cgns_scalar import cgns_scalar as cgns_scalar_cls
class cgns(Command):
    """
    Write a CGNS file.
    
    Parameters
    ----------
        name : str
            'name' child.
        scope : str
            'scope' child.
        cell_zones : typing.List[str]
            'cell_zones' child.
        surfaces : typing.List[str]
            'surfaces' child.
        cell_centered : bool
            'cell_centered' child.
        format_class : str
            'format_class' child.
        cgns_scalar : typing.List[str]
            'cgns_scalar' child.
    
    """

    fluent_name = "cgns"

    argument_names = \
        ['name', 'scope', 'cell_zones', 'surfaces', 'cell_centered',
         'format_class', 'cgns_scalar']

    name: name_cls = name_cls
    """
    name argument of cgns.
    """
    scope: scope_cls = scope_cls
    """
    scope argument of cgns.
    """
    cell_zones: cell_zones_cls = cell_zones_cls
    """
    cell_zones argument of cgns.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces argument of cgns.
    """
    cell_centered: cell_centered_cls = cell_centered_cls
    """
    cell_centered argument of cgns.
    """
    format_class: format_class_cls = format_class_cls
    """
    format_class argument of cgns.
    """
    cgns_scalar: cgns_scalar_cls = cgns_scalar_cls
    """
    cgns_scalar argument of cgns.
    """
