#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .lines import lines as lines_cls
from .markers import markers as markers_cls
class curves(Group):
    """
    'curves' child.
    """

    fluent_name = "curves"

    child_names = \
        ['lines', 'markers']

    lines: lines_cls = lines_cls
    """
    lines child of curves.
    """
    markers: markers_cls = markers_cls
    """
    markers child of curves.
    """
