#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .include_pop_in_fsi_force import include_pop_in_fsi_force as include_pop_in_fsi_force_cls
from .steady_2way_fsi import steady_2way_fsi as steady_2way_fsi_cls
from .include_viscous_fsi_force import include_viscous_fsi_force as include_viscous_fsi_force_cls
from .explicit_fsi_force import explicit_fsi_force as explicit_fsi_force_cls
from .starting_t_re_initialization import starting_t_re_initialization as starting_t_re_initialization_cls
class expert(Group):
    """
    Enter the structure expert menu.
    """

    fluent_name = "expert"

    child_names = \
        ['include_pop_in_fsi_force', 'steady_2way_fsi',
         'include_viscous_fsi_force', 'explicit_fsi_force',
         'starting_t_re_initialization']

    include_pop_in_fsi_force: include_pop_in_fsi_force_cls = include_pop_in_fsi_force_cls
    """
    include_pop_in_fsi_force child of expert.
    """
    steady_2way_fsi: steady_2way_fsi_cls = steady_2way_fsi_cls
    """
    steady_2way_fsi child of expert.
    """
    include_viscous_fsi_force: include_viscous_fsi_force_cls = include_viscous_fsi_force_cls
    """
    include_viscous_fsi_force child of expert.
    """
    explicit_fsi_force: explicit_fsi_force_cls = explicit_fsi_force_cls
    """
    explicit_fsi_force child of expert.
    """
    starting_t_re_initialization: starting_t_re_initialization_cls = starting_t_re_initialization_cls
    """
    starting_t_re_initialization child of expert.
    """
