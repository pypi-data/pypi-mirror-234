#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .display import display as display_cls
from .vector_child import vector_child

class vector(NamedObject[vector_child], _CreatableNamedObjectMixin[vector_child]):
    """
    'vector' child.
    """

    fluent_name = "vector"

    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of vector.
    """
    child_object_type: vector_child = vector_child
    """
    child_object_type of vector.
    """
