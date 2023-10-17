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
from .single_rate import single_rate as single_rate_cls
from .two_competing_rates import two_competing_rates as two_competing_rates_cls
from .cpd_model import cpd_model as cpd_model_cls
class devolatilization_model(Group):
    """
    'devolatilization_model' child.
    """

    fluent_name = "devolatilization-model"

    child_names = \
        ['option', 'value', 'single_rate', 'two_competing_rates', 'cpd_model']

    option: option_cls = option_cls
    """
    option child of devolatilization_model.
    """
    value: value_cls = value_cls
    """
    value child of devolatilization_model.
    """
    single_rate: single_rate_cls = single_rate_cls
    """
    single_rate child of devolatilization_model.
    """
    two_competing_rates: two_competing_rates_cls = two_competing_rates_cls
    """
    two_competing_rates child of devolatilization_model.
    """
    cpd_model: cpd_model_cls = cpd_model_cls
    """
    cpd_model child of devolatilization_model.
    """
