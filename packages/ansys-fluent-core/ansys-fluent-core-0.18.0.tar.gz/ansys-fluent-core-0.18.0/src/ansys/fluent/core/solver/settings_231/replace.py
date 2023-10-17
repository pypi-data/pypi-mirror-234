#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .zones import zones as zones_cls
class replace(Command):
    """
    Replace mesh and interpolate data.
    
    Parameters
    ----------
        name : str
            'name' child.
        zones : bool
            'zones' child.
    
    """

    fluent_name = "replace"

    argument_names = \
        ['name', 'zones']

    name: name_cls = name_cls
    """
    name argument of replace.
    """
    zones: zones_cls = zones_cls
    """
    zones argument of replace.
    """
