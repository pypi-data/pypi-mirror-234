#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_11 import phase as phase_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature_1 import temperature as temperature_cls
from .q import q as q_cls
class network_end_child(Group):
    """
    'child_object_type' of network_end.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'thermal_bc', 'temperature', 'q']

    phase: phase_cls = phase_cls
    """
    phase child of network_end_child.
    """
    thermal_bc: thermal_bc_cls = thermal_bc_cls
    """
    thermal_bc child of network_end_child.
    """
    temperature: temperature_cls = temperature_cls
    """
    temperature child of network_end_child.
    """
    q: q_cls = q_cls
    """
    q child of network_end_child.
    """
