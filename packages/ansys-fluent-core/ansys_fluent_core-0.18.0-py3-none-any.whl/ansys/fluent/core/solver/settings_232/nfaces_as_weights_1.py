#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .nfaces_as_weights import nfaces_as_weights as nfaces_as_weights_cls
from .user_defined_value import user_defined_value as user_defined_value_cls
from .value_1 import value as value_cls
class nfaces_as_weights(Group):
    """
    Use number of faces as weights.
    """

    fluent_name = "nfaces-as-weights"

    child_names = \
        ['nfaces_as_weights', 'user_defined_value', 'value']

    nfaces_as_weights: nfaces_as_weights_cls = nfaces_as_weights_cls
    """
    nfaces_as_weights child of nfaces_as_weights.
    """
    user_defined_value: user_defined_value_cls = user_defined_value_cls
    """
    user_defined_value child of nfaces_as_weights.
    """
    value: value_cls = value_cls
    """
    value child of nfaces_as_weights.
    """
