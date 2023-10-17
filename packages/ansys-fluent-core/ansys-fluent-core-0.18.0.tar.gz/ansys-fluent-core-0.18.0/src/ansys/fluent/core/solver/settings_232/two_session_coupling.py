#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_6 import method as method_cls
from .type_2 import type as type_cls
from .frequency_1 import frequency as frequency_cls
class two_session_coupling(Group):
    """
    'two_session_coupling' child.
    """

    fluent_name = "two-session-coupling"

    child_names = \
        ['method', 'type', 'frequency']

    method: method_cls = method_cls
    """
    method child of two_session_coupling.
    """
    type: type_cls = type_cls
    """
    type child of two_session_coupling.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of two_session_coupling.
    """
