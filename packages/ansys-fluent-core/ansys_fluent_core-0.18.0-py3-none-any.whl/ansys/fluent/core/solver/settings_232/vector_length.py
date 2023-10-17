#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .constant_length import constant_length as constant_length_cls
from .variable_length import variable_length as variable_length_cls
class vector_length(Group):
    """
    'vector_length' child.
    """

    fluent_name = "vector-length"

    child_names = \
        ['option', 'constant_length', 'variable_length']

    option: option_cls = option_cls
    """
    option child of vector_length.
    """
    constant_length: constant_length_cls = constant_length_cls
    """
    constant_length child of vector_length.
    """
    variable_length: variable_length_cls = variable_length_cls
    """
    variable_length child of vector_length.
    """
