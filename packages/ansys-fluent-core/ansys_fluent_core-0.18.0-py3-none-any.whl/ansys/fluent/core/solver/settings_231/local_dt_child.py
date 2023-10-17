#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_pseudo_time_method import enable_pseudo_time_method as enable_pseudo_time_method_cls
from .pseudo_time_scale_factor import pseudo_time_scale_factor as pseudo_time_scale_factor_cls
from .implicit_under_relaxation_factor import implicit_under_relaxation_factor as implicit_under_relaxation_factor_cls
class local_dt_child(Group):
    """
    'child_object_type' of local_dt.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['enable_pseudo_time_method', 'pseudo_time_scale_factor',
         'implicit_under_relaxation_factor']

    enable_pseudo_time_method: enable_pseudo_time_method_cls = enable_pseudo_time_method_cls
    """
    enable_pseudo_time_method child of local_dt_child.
    """
    pseudo_time_scale_factor: pseudo_time_scale_factor_cls = pseudo_time_scale_factor_cls
    """
    pseudo_time_scale_factor child of local_dt_child.
    """
    implicit_under_relaxation_factor: implicit_under_relaxation_factor_cls = implicit_under_relaxation_factor_cls
    """
    implicit_under_relaxation_factor child of local_dt_child.
    """
