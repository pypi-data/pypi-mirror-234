#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mass_flux_correction_method import mass_flux_correction_method as mass_flux_correction_method_cls
from .hybrid_mode_selection import hybrid_mode_selection as hybrid_mode_selection_cls
class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['mass_flux_correction_method', 'hybrid_mode_selection']

    mass_flux_correction_method: mass_flux_correction_method_cls = mass_flux_correction_method_cls
    """
    mass_flux_correction_method child of expert.
    """
    hybrid_mode_selection: hybrid_mode_selection_cls = hybrid_mode_selection_cls
    """
    hybrid_mode_selection child of expert.
    """
