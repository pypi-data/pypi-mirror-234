#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .const_htc import const_htc as const_htc_cls
from .const_nu import const_nu as const_nu_cls
class heat_exchange(Group):
    """
    'heat_exchange' child.
    """

    fluent_name = "heat-exchange"

    child_names = \
        ['option', 'const_htc', 'const_nu']

    option: option_cls = option_cls
    """
    option child of heat_exchange.
    """
    const_htc: const_htc_cls = const_htc_cls
    """
    const_htc child of heat_exchange.
    """
    const_nu: const_nu_cls = const_nu_cls
    """
    const_nu child of heat_exchange.
    """
