#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .low_order_rhie_chow import low_order_rhie_chow as low_order_rhie_chow_cls
class rhie_chow_flux(Group):
    """
    'rhie_chow_flux' child.
    """

    fluent_name = "rhie-chow-flux"

    child_names = \
        ['low_order_rhie_chow']

    low_order_rhie_chow: low_order_rhie_chow_cls = low_order_rhie_chow_cls
    """
    low_order_rhie_chow child of rhie_chow_flux.
    """
