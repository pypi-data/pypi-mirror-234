#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .flow_scheme import flow_scheme as flow_scheme_cls
from .coupled_form import coupled_form as coupled_form_cls
from .solve_n_phase import solve_n_phase as solve_n_phase_cls
class p_v_coupling(Group):
    """
    Select the pressure velocity coupling scheme.
    """

    fluent_name = "p-v-coupling"

    child_names = \
        ['flow_scheme', 'coupled_form', 'solve_n_phase']

    flow_scheme: flow_scheme_cls = flow_scheme_cls
    """
    flow_scheme child of p_v_coupling.
    """
    coupled_form: coupled_form_cls = coupled_form_cls
    """
    coupled_form child of p_v_coupling.
    """
    solve_n_phase: solve_n_phase_cls = solve_n_phase_cls
    """
    solve_n_phase child of p_v_coupling.
    """
