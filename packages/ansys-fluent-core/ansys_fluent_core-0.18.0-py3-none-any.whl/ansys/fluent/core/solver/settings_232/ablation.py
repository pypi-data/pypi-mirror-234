#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_1 import enabled as enabled_cls
class ablation(Group):
    """
    'ablation' child.
    """

    fluent_name = "ablation"

    child_names = \
        ['enabled']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of ablation.
    """
