#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .thin_film import thin_film as thin_film_cls
from .liquid_vof_factor import liquid_vof_factor as liquid_vof_factor_cls
class boiling_parameters(Group):
    """
    Multiphase boiling parameters menu.
    """

    fluent_name = "boiling-parameters"

    child_names = \
        ['thin_film', 'liquid_vof_factor']

    thin_film: thin_film_cls = thin_film_cls
    """
    thin_film child of boiling_parameters.
    """
    liquid_vof_factor: liquid_vof_factor_cls = liquid_vof_factor_cls
    """
    liquid_vof_factor child of boiling_parameters.
    """
