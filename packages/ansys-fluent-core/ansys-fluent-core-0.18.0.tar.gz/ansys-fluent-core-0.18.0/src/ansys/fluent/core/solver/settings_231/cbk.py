#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .char_intrinsic_reactivity import char_intrinsic_reactivity as char_intrinsic_reactivity_cls
from .carbon_content_percentage import carbon_content_percentage as carbon_content_percentage_cls
class cbk(Group):
    """
    'cbk' child.
    """

    fluent_name = "cbk"

    child_names = \
        ['option', 'char_intrinsic_reactivity', 'carbon_content_percentage']

    option: option_cls = option_cls
    """
    option child of cbk.
    """
    char_intrinsic_reactivity: char_intrinsic_reactivity_cls = char_intrinsic_reactivity_cls
    """
    char_intrinsic_reactivity child of cbk.
    """
    carbon_content_percentage: carbon_content_percentage_cls = carbon_content_percentage_cls
    """
    carbon_content_percentage child of cbk.
    """
