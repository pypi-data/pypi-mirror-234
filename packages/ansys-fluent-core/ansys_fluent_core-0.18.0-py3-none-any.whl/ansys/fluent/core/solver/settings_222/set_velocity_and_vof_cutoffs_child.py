#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .max_vol_mag import max_vol_mag as max_vol_mag_cls
from .vol_frac_cutoff import vol_frac_cutoff as vol_frac_cutoff_cls
class set_velocity_and_vof_cutoffs_child(Group):
    """
    'child_object_type' of set_velocity_and_vof_cutoffs.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['max_vol_mag', 'vol_frac_cutoff']

    max_vol_mag: max_vol_mag_cls = max_vol_mag_cls
    """
    max_vol_mag child of set_velocity_and_vof_cutoffs_child.
    """
    vol_frac_cutoff: vol_frac_cutoff_cls = vol_frac_cutoff_cls
    """
    vol_frac_cutoff child of set_velocity_and_vof_cutoffs_child.
    """
