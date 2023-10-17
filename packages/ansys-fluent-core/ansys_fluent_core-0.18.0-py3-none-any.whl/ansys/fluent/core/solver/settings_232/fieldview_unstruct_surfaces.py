#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .options import options as options_cls
from .name import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls
class fieldview_unstruct_surfaces(Command):
    """
    Write a Fieldview unstructured surface mesh, data.
    
    Parameters
    ----------
        options : str
            'options' child.
        name : str
            'name' child.
        surfaces : typing.List[str]
            'surfaces' child.
        cell_func_domain : typing.List[str]
            'cell_func_domain' child.
    
    """

    fluent_name = "fieldview-unstruct-surfaces"

    argument_names = \
        ['options', 'name', 'surfaces', 'cell_func_domain']

    options: options_cls = options_cls
    """
    options argument of fieldview_unstruct_surfaces.
    """
    name: name_cls = name_cls
    """
    name argument of fieldview_unstruct_surfaces.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces argument of fieldview_unstruct_surfaces.
    """
    cell_func_domain: cell_func_domain_cls = cell_func_domain_cls
    """
    cell_func_domain argument of fieldview_unstruct_surfaces.
    """
