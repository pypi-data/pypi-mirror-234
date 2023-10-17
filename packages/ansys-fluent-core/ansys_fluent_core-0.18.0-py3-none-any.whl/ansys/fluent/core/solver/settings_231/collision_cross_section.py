#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .cross_section_multicomponent import cross_section_multicomponent as cross_section_multicomponent_cls
class collision_cross_section(Group):
    """
    'collision_cross_section' child.
    """

    fluent_name = "collision-cross-section"

    child_names = \
        ['option', 'cross_section_multicomponent']

    option: option_cls = option_cls
    """
    option child of collision_cross_section.
    """
    cross_section_multicomponent: cross_section_multicomponent_cls = cross_section_multicomponent_cls
    """
    cross_section_multicomponent child of collision_cross_section.
    """
