#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pole import pole as pole_cls
from .amplitude import amplitude as amplitude_cls
class impedance_1_child(Group):
    """
    'child_object_type' of impedance_1.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pole', 'amplitude']

    pole: pole_cls = pole_cls
    """
    pole child of impedance_1_child.
    """
    amplitude: amplitude_cls = amplitude_cls
    """
    amplitude child of impedance_1_child.
    """
