#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .origin import origin as origin_cls
from .orientation import orientation as orientation_cls
class initial_state(Group):
    """
    'initial_state' child.
    """

    fluent_name = "initial-state"

    child_names = \
        ['origin', 'orientation']

    origin: origin_cls = origin_cls
    """
    origin child of initial_state.
    """
    orientation: orientation_cls = orientation_cls
    """
    orientation child of initial_state.
    """
