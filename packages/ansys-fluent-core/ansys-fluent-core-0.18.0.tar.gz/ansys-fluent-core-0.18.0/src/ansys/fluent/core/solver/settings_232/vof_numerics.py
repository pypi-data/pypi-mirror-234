#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .high_order_rc import high_order_rc as high_order_rc_cls
from .high_order_rc_hybrid_treatment import high_order_rc_hybrid_treatment as high_order_rc_hybrid_treatment_cls
from .force_treatment_of_unsteady_rc import force_treatment_of_unsteady_rc as force_treatment_of_unsteady_rc_cls
from .unstructured_var_presto_scheme import unstructured_var_presto_scheme as unstructured_var_presto_scheme_cls
from .new_framework_for_vof_specific_node_based_treatment import new_framework_for_vof_specific_node_based_treatment as new_framework_for_vof_specific_node_based_treatment_cls
class vof_numerics(Group):
    """
    Set VOF numeric options.
    """

    fluent_name = "vof-numerics"

    child_names = \
        ['high_order_rc', 'high_order_rc_hybrid_treatment',
         'force_treatment_of_unsteady_rc', 'unstructured_var_presto_scheme',
         'new_framework_for_vof_specific_node_based_treatment']

    high_order_rc: high_order_rc_cls = high_order_rc_cls
    """
    high_order_rc child of vof_numerics.
    """
    high_order_rc_hybrid_treatment: high_order_rc_hybrid_treatment_cls = high_order_rc_hybrid_treatment_cls
    """
    high_order_rc_hybrid_treatment child of vof_numerics.
    """
    force_treatment_of_unsteady_rc: force_treatment_of_unsteady_rc_cls = force_treatment_of_unsteady_rc_cls
    """
    force_treatment_of_unsteady_rc child of vof_numerics.
    """
    unstructured_var_presto_scheme: unstructured_var_presto_scheme_cls = unstructured_var_presto_scheme_cls
    """
    unstructured_var_presto_scheme child of vof_numerics.
    """
    new_framework_for_vof_specific_node_based_treatment: new_framework_for_vof_specific_node_based_treatment_cls = new_framework_for_vof_specific_node_based_treatment_cls
    """
    new_framework_for_vof_specific_node_based_treatment child of vof_numerics.
    """
