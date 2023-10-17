#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .high_order_pressure import high_order_pressure as high_order_pressure_cls
from .interpolation_method import interpolation_method as interpolation_method_cls
from .orphan_cell_treatment import orphan_cell_treatment as orphan_cell_treatment_cls
from .expert_3 import expert as expert_cls
class overset(Group):
    """
    Enter overset solver options menu.
    """

    fluent_name = "overset"

    child_names = \
        ['high_order_pressure', 'interpolation_method',
         'orphan_cell_treatment', 'expert']

    high_order_pressure: high_order_pressure_cls = high_order_pressure_cls
    """
    high_order_pressure child of overset.
    """
    interpolation_method: interpolation_method_cls = interpolation_method_cls
    """
    interpolation_method child of overset.
    """
    orphan_cell_treatment: orphan_cell_treatment_cls = orphan_cell_treatment_cls
    """
    orphan_cell_treatment child of overset.
    """
    expert: expert_cls = expert_cls
    """
    expert child of overset.
    """
