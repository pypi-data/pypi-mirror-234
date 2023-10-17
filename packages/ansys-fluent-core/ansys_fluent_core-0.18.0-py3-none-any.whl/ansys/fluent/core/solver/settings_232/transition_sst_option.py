#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_roughness_correlation import enable_roughness_correlation as enable_roughness_correlation_cls
from .roughness_correlation_fcn import roughness_correlation_fcn as roughness_correlation_fcn_cls
from .geometric_roughness_ht_val import geometric_roughness_ht_val as geometric_roughness_ht_val_cls
class transition_sst_option(Group):
    """
    'transition_sst_option' child.
    """

    fluent_name = "transition-sst-option"

    child_names = \
        ['enable_roughness_correlation', 'roughness_correlation_fcn',
         'geometric_roughness_ht_val']

    enable_roughness_correlation: enable_roughness_correlation_cls = enable_roughness_correlation_cls
    """
    enable_roughness_correlation child of transition_sst_option.
    """
    roughness_correlation_fcn: roughness_correlation_fcn_cls = roughness_correlation_fcn_cls
    """
    roughness_correlation_fcn child of transition_sst_option.
    """
    geometric_roughness_ht_val: geometric_roughness_ht_val_cls = geometric_roughness_ht_val_cls
    """
    geometric_roughness_ht_val child of transition_sst_option.
    """
