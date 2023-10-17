#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_5 import option as option_cls
from .partitioning_method_for_dpm_domain import partitioning_method_for_dpm_domain as partitioning_method_for_dpm_domain_cls
class dpm_domain(Group):
    """
    'dpm_domain' child.
    """

    fluent_name = "dpm-domain"

    child_names = \
        ['option', 'partitioning_method_for_dpm_domain']

    option: option_cls = option_cls
    """
    option child of dpm_domain.
    """
    partitioning_method_for_dpm_domain: partitioning_method_for_dpm_domain_cls = partitioning_method_for_dpm_domain_cls
    """
    partitioning_method_for_dpm_domain child of dpm_domain.
    """
