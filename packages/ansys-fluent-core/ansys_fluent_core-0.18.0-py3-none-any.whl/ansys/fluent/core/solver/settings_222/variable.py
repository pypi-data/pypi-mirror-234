#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .size_by import size_by as size_by_cls
from .range import range as range_cls
class variable(Group):
    """
    'variable' child.
    """

    fluent_name = "variable"

    child_names = \
        ['size_by', 'range']

    size_by: size_by_cls = size_by_cls
    """
    size_by child of variable.
    """
    range: range_cls = range_cls
    """
    range child of variable.
    """
