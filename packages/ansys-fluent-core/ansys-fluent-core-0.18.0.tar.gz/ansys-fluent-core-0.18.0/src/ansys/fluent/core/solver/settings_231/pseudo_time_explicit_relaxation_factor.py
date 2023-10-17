#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .local_dt_dualts_relax import local_dt_dualts_relax as local_dt_dualts_relax_cls
from .global_dt_pseudo_relax import global_dt_pseudo_relax as global_dt_pseudo_relax_cls
class pseudo_time_explicit_relaxation_factor(Group):
    """
    'pseudo_time_explicit_relaxation_factor' child.
    """

    fluent_name = "pseudo-time-explicit-relaxation-factor"

    child_names = \
        ['local_dt_dualts_relax', 'global_dt_pseudo_relax']

    local_dt_dualts_relax: local_dt_dualts_relax_cls = local_dt_dualts_relax_cls
    """
    local_dt_dualts_relax child of pseudo_time_explicit_relaxation_factor.
    """
    global_dt_pseudo_relax: global_dt_pseudo_relax_cls = global_dt_pseudo_relax_cls
    """
    global_dt_pseudo_relax child of pseudo_time_explicit_relaxation_factor.
    """
