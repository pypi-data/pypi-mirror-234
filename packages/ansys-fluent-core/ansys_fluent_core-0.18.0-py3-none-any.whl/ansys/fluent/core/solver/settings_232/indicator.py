#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .indicator_type import indicator_type as indicator_type_cls
from .single_scalar_fn import single_scalar_fn as single_scalar_fn_cls
from .multi_scalar_fn import multi_scalar_fn as multi_scalar_fn_cls
class indicator(Group):
    """
    Set the indicator type and variable(s) for anisotropic adaption.
    """

    fluent_name = "indicator"

    child_names = \
        ['indicator_type', 'single_scalar_fn', 'multi_scalar_fn']

    indicator_type: indicator_type_cls = indicator_type_cls
    """
    indicator_type child of indicator.
    """
    single_scalar_fn: single_scalar_fn_cls = single_scalar_fn_cls
    """
    single_scalar_fn child of indicator.
    """
    multi_scalar_fn: multi_scalar_fn_cls = multi_scalar_fn_cls
    """
    multi_scalar_fn child of indicator.
    """
