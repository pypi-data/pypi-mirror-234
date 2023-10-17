#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
class reaction_model(Group):
    """
    'reaction_model' child.
    """

    fluent_name = "reaction-model"

    child_names = \
        ['option']

    option: option_cls = option_cls
    """
    option child of reaction_model.
    """
