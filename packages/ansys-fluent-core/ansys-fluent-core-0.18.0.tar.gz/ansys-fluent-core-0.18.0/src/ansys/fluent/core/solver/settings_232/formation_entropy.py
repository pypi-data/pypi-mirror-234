#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .value_1 import value as value_cls
class formation_entropy(Group):
    """
    'formation_entropy' child.
    """

    fluent_name = "formation-entropy"

    child_names = \
        ['option', 'value']

    option: option_cls = option_cls
    """
    option child of formation_entropy.
    """
    value: value_cls = value_cls
    """
    value child of formation_entropy.
    """
