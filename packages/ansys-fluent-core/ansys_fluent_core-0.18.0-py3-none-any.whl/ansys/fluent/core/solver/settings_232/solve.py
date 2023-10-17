#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .iterate_1 import iterate as iterate_cls
from .dual_time_iterate_1 import dual_time_iterate as dual_time_iterate_cls
class solve(Group):
    """
    'solve' child.
    """

    fluent_name = "solve"

    command_names = \
        ['iterate', 'dual_time_iterate']

    iterate: iterate_cls = iterate_cls
    """
    iterate command of solve.
    """
    dual_time_iterate: dual_time_iterate_cls = dual_time_iterate_cls
    """
    dual_time_iterate command of solve.
    """
