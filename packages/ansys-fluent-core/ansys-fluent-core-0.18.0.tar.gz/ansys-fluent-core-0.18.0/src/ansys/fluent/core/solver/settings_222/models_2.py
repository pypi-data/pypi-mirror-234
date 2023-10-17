#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .model_ramping import model_ramping as model_ramping_cls
from .ramp_flow import ramp_flow as ramp_flow_cls
from .ramp_turbulence import ramp_turbulence as ramp_turbulence_cls
from .ramp_scalars import ramp_scalars as ramp_scalars_cls
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['model_ramping', 'ramp_flow', 'ramp_turbulence', 'ramp_scalars']

    model_ramping: model_ramping_cls = model_ramping_cls
    """
    model_ramping child of models.
    """
    ramp_flow: ramp_flow_cls = ramp_flow_cls
    """
    ramp_flow child of models.
    """
    ramp_turbulence: ramp_turbulence_cls = ramp_turbulence_cls
    """
    ramp_turbulence child of models.
    """
    ramp_scalars: ramp_scalars_cls = ramp_scalars_cls
    """
    ramp_scalars child of models.
    """
