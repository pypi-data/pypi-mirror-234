#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use import use as use_cls
from .use_user_define_value import use_user_define_value as use_user_define_value_cls
from .value import value as value_cls
class solid_thread_weight(Group):
    """
    Use solid thread weights.
    """

    fluent_name = "solid-thread-weight"

    child_names = \
        ['use', 'use_user_define_value', 'value']

    use: use_cls = use_cls
    """
    use child of solid_thread_weight.
    """
    use_user_define_value: use_user_define_value_cls = use_user_define_value_cls
    """
    use_user_define_value child of solid_thread_weight.
    """
    value: value_cls = value_cls
    """
    value child of solid_thread_weight.
    """
