#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .viscous_scale import viscous_scale as viscous_scale_cls
from .gravity_scale import gravity_scale as gravity_scale_cls
from .surface_tension_scale import surface_tension_scale as surface_tension_scale_cls
from .acoustic_scale import acoustic_scale as acoustic_scale_cls
class time_scale_options(Group):
    """
    'time_scale_options' child.
    """

    fluent_name = "time-scale-options"

    child_names = \
        ['viscous_scale', 'gravity_scale', 'surface_tension_scale',
         'acoustic_scale']

    viscous_scale: viscous_scale_cls = viscous_scale_cls
    """
    viscous_scale child of time_scale_options.
    """
    gravity_scale: gravity_scale_cls = gravity_scale_cls
    """
    gravity_scale child of time_scale_options.
    """
    surface_tension_scale: surface_tension_scale_cls = surface_tension_scale_cls
    """
    surface_tension_scale child of time_scale_options.
    """
    acoustic_scale: acoustic_scale_cls = acoustic_scale_cls
    """
    acoustic_scale child of time_scale_options.
    """
