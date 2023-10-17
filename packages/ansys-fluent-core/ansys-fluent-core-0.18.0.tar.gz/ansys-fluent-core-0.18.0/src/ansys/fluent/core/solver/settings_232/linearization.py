#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .keep_linearized_source_terms_constant import keep_linearized_source_terms_constant as keep_linearized_source_terms_constant_cls
from .source_term_linearization_enabled import source_term_linearization_enabled as source_term_linearization_enabled_cls
from .enhanced_linearization_enabled import enhanced_linearization_enabled as enhanced_linearization_enabled_cls
from .linearized_source_terms_limiter import linearized_source_terms_limiter as linearized_source_terms_limiter_cls
class linearization(Group):
    """
    Menu containing options to enable/disable linearization of DPM source terms. 
    Please note that source term linearization is only available if the node-based averaging option is not active.
    """

    fluent_name = "linearization"

    child_names = \
        ['keep_linearized_source_terms_constant',
         'source_term_linearization_enabled',
         'enhanced_linearization_enabled', 'linearized_source_terms_limiter']

    keep_linearized_source_terms_constant: keep_linearized_source_terms_constant_cls = keep_linearized_source_terms_constant_cls
    """
    keep_linearized_source_terms_constant child of linearization.
    """
    source_term_linearization_enabled: source_term_linearization_enabled_cls = source_term_linearization_enabled_cls
    """
    source_term_linearization_enabled child of linearization.
    """
    enhanced_linearization_enabled: enhanced_linearization_enabled_cls = enhanced_linearization_enabled_cls
    """
    enhanced_linearization_enabled child of linearization.
    """
    linearized_source_terms_limiter: linearized_source_terms_limiter_cls = linearized_source_terms_limiter_cls
    """
    linearized_source_terms_limiter child of linearization.
    """
