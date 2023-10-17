#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .dispersion_force_in_momentum import dispersion_force_in_momentum as dispersion_force_in_momentum_cls
from .dispersion_in_relative_velocity import dispersion_in_relative_velocity as dispersion_in_relative_velocity_cls
class multiphase_options(Group):
    """
    'multiphase_options' child.
    """

    fluent_name = "multiphase-options"

    child_names = \
        ['dispersion_force_in_momentum', 'dispersion_in_relative_velocity']

    dispersion_force_in_momentum: dispersion_force_in_momentum_cls = dispersion_force_in_momentum_cls
    """
    dispersion_force_in_momentum child of multiphase_options.
    """
    dispersion_in_relative_velocity: dispersion_in_relative_velocity_cls = dispersion_in_relative_velocity_cls
    """
    dispersion_in_relative_velocity child of multiphase_options.
    """
