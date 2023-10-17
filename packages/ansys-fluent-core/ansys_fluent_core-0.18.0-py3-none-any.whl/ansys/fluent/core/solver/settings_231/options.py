#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .migrate_and_reorder import migrate_and_reorder as migrate_and_reorder_cls
from .preserve_boundary_layer import preserve_boundary_layer as preserve_boundary_layer_cls
from .preserve_interior_zones import preserve_interior_zones as preserve_interior_zones_cls
class options(Group):
    """
    Enter options menu.
    """

    fluent_name = "options"

    child_names = \
        ['migrate_and_reorder', 'preserve_boundary_layer',
         'preserve_interior_zones']

    migrate_and_reorder: migrate_and_reorder_cls = migrate_and_reorder_cls
    """
    migrate_and_reorder child of options.
    """
    preserve_boundary_layer: preserve_boundary_layer_cls = preserve_boundary_layer_cls
    """
    preserve_boundary_layer child of options.
    """
    preserve_interior_zones: preserve_interior_zones_cls = preserve_interior_zones_cls
    """
    preserve_interior_zones child of options.
    """
