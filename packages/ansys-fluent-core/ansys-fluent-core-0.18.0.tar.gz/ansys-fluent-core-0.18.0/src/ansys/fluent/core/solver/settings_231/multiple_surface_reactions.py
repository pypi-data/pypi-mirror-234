#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .composition_dependent_specific_heat import composition_dependent_specific_heat as composition_dependent_specific_heat_cls
from .composition_dependent_density import composition_dependent_density as composition_dependent_density_cls
class multiple_surface_reactions(Group):
    """
    'multiple_surface_reactions' child.
    """

    fluent_name = "multiple-surface-reactions"

    child_names = \
        ['composition_dependent_specific_heat',
         'composition_dependent_density']

    composition_dependent_specific_heat: composition_dependent_specific_heat_cls = composition_dependent_specific_heat_cls
    """
    composition_dependent_specific_heat child of multiple_surface_reactions.
    """
    composition_dependent_density: composition_dependent_density_cls = composition_dependent_density_cls
    """
    composition_dependent_density child of multiple_surface_reactions.
    """
