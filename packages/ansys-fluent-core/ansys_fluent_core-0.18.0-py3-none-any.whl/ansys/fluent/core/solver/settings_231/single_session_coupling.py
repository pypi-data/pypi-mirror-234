#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .method_4 import method as method_cls
from .type_1 import type as type_cls
from .interval_1 import interval as interval_cls
from .frequency_1 import frequency as frequency_cls
class single_session_coupling(Group):
    """
    'single_session_coupling' child.
    """

    fluent_name = "single-session-coupling"

    child_names = \
        ['method', 'type', 'interval', 'frequency']

    method: method_cls = method_cls
    """
    method child of single_session_coupling.
    """
    type: type_cls = type_cls
    """
    type child of single_session_coupling.
    """
    interval: interval_cls = interval_cls
    """
    interval child of single_session_coupling.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of single_session_coupling.
    """
