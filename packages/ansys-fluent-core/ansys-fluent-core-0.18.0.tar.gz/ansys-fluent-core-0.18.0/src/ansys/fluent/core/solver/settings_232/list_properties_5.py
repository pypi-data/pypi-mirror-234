#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .register_name import register_name as register_name_cls
class list_properties(Command):
    """
    List the properties of a definition for poor mesh numerics.
    
    Parameters
    ----------
        register_name : str
            'register_name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['register_name']

    register_name: register_name_cls = register_name_cls
    """
    register_name argument of list_properties.
    """
