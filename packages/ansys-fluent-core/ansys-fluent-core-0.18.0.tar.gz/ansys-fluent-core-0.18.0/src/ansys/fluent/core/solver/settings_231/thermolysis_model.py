#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .single_rate import single_rate as single_rate_cls
from .secondary_rate import secondary_rate as secondary_rate_cls
from .value import value as value_cls
class thermolysis_model(Group):
    """
    'thermolysis_model' child.
    """

    fluent_name = "thermolysis-model"

    child_names = \
        ['option', 'single_rate', 'secondary_rate', 'value']

    option: option_cls = option_cls
    """
    option child of thermolysis_model.
    """
    single_rate: single_rate_cls = single_rate_cls
    """
    single_rate child of thermolysis_model.
    """
    secondary_rate: secondary_rate_cls = secondary_rate_cls
    """
    secondary_rate child of thermolysis_model.
    """
    value: value_cls = value_cls
    """
    value child of thermolysis_model.
    """
