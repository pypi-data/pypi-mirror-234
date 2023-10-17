#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .growth_ratio_refinement import growth_ratio_refinement as growth_ratio_refinement_cls
class type(Group):
    """
    'type' child.
    """

    fluent_name = "type"

    child_names = \
        ['option', 'growth_ratio_refinement']

    option: option_cls = option_cls
    """
    option child of type.
    """
    growth_ratio_refinement: growth_ratio_refinement_cls = growth_ratio_refinement_cls
    """
    growth_ratio_refinement child of type.
    """
