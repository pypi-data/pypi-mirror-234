#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .band_width import band_width as band_width_cls
from .reorder_domain import reorder_domain as reorder_domain_cls
from .reorder_zones import reorder_zones as reorder_zones_cls
class reorder(Group):
    """
    Enter the reorder domain menu.
    """

    fluent_name = "reorder"

    command_names = \
        ['band_width', 'reorder_domain', 'reorder_zones']

    band_width: band_width_cls = band_width_cls
    """
    band_width command of reorder.
    """
    reorder_domain: reorder_domain_cls = reorder_domain_cls
    """
    reorder_domain command of reorder.
    """
    reorder_zones: reorder_zones_cls = reorder_zones_cls
    """
    reorder_zones command of reorder.
    """
