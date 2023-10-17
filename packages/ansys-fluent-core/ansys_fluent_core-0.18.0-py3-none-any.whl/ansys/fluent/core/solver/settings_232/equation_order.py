#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .solve_flow_last import solve_flow_last as solve_flow_last_cls
from .solve_exp_vof_at_end import solve_exp_vof_at_end as solve_exp_vof_at_end_cls
class equation_order(Group):
    """
    Equation Order Menu for Homogeneous Multiphase Flow Models.
    """

    fluent_name = "equation-order"

    child_names = \
        ['solve_flow_last', 'solve_exp_vof_at_end']

    solve_flow_last: solve_flow_last_cls = solve_flow_last_cls
    """
    solve_flow_last child of equation_order.
    """
    solve_exp_vof_at_end: solve_exp_vof_at_end_cls = solve_exp_vof_at_end_cls
    """
    solve_exp_vof_at_end child of equation_order.
    """
