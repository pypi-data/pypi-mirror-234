#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .step_size import step_size as step_size_cls
from .tolerance import tolerance as tolerance_cls
class accuracy_control(Group):
    """
    'accuracy_control' child.
    """

    fluent_name = "accuracy-control"

    child_names = \
        ['option', 'step_size', 'tolerance']

    option: option_cls = option_cls
    """
    option child of accuracy_control.
    """
    step_size: step_size_cls = step_size_cls
    """
    step_size child of accuracy_control.
    """
    tolerance: tolerance_cls = tolerance_cls
    """
    tolerance child of accuracy_control.
    """
