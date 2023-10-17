#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature import temperature as temperature_cls
from .q import q as q_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['thermal_bc', 'temperature', 'q']

    thermal_bc: thermal_bc_cls = thermal_bc_cls
    """
    thermal_bc child of phase_child.
    """
    temperature: temperature_cls = temperature_cls
    """
    temperature child of phase_child.
    """
    q: q_cls = q_cls
    """
    q child of phase_child.
    """
