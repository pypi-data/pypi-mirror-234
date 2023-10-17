#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .type_1 import type as type_cls
from .name import name as name_cls
class copy_database_material_by_name(Command):
    """
    'copy_database_material_by_name' command.
    
    Parameters
    ----------
        type : str
            'type' child.
        name : str
            'name' child.
    
    """

    fluent_name = "copy-database-material-by-name"

    argument_names = \
        ['type', 'name']

    type: type_cls = type_cls
    """
    type argument of copy_database_material_by_name.
    """
    name: name_cls = name_cls
    """
    name argument of copy_database_material_by_name.
    """
