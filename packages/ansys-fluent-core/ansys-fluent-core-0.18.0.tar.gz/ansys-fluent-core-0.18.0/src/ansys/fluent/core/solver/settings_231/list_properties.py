#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
class list_properties(Command):
    """
    List the properties of a material in the database.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['name']

    name: name_cls = name_cls
    """
    name argument of list_properties.
    """
