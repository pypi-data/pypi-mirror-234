#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .global_range import global_range as global_range_cls
class auto_range_on(Group):
    """
    'auto_range_on' child.
    """

    fluent_name = "auto-range-on"

    child_names = \
        ['global_range']

    global_range: global_range_cls = global_range_cls
    """
    global_range child of auto_range_on.
    """
