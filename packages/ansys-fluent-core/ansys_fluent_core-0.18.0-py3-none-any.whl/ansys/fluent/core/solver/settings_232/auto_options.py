#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .proximity_tolerance import proximity_tolerance as proximity_tolerance_cls
from .set_default_name_prefix import set_default_name_prefix as set_default_name_prefix_cls
from .set_one_to_one_pairing_tolerance import set_one_to_one_pairing_tolerance as set_one_to_one_pairing_tolerance_cls
from .pairing_between_different_cell_zones_only import pairing_between_different_cell_zones_only as pairing_between_different_cell_zones_only_cls
from .pairing_between_interface_zones_only import pairing_between_interface_zones_only as pairing_between_interface_zones_only_cls
from .keep_empty_interface import keep_empty_interface as keep_empty_interface_cls
from .naming_option import naming_option as naming_option_cls
class auto_options(Group):
    """
    Enter auto-options menu.
    """

    fluent_name = "auto-options"

    child_names = \
        ['proximity_tolerance', 'set_default_name_prefix',
         'set_one_to_one_pairing_tolerance',
         'pairing_between_different_cell_zones_only',
         'pairing_between_interface_zones_only', 'keep_empty_interface']

    proximity_tolerance: proximity_tolerance_cls = proximity_tolerance_cls
    """
    proximity_tolerance child of auto_options.
    """
    set_default_name_prefix: set_default_name_prefix_cls = set_default_name_prefix_cls
    """
    set_default_name_prefix child of auto_options.
    """
    set_one_to_one_pairing_tolerance: set_one_to_one_pairing_tolerance_cls = set_one_to_one_pairing_tolerance_cls
    """
    set_one_to_one_pairing_tolerance child of auto_options.
    """
    pairing_between_different_cell_zones_only: pairing_between_different_cell_zones_only_cls = pairing_between_different_cell_zones_only_cls
    """
    pairing_between_different_cell_zones_only child of auto_options.
    """
    pairing_between_interface_zones_only: pairing_between_interface_zones_only_cls = pairing_between_interface_zones_only_cls
    """
    pairing_between_interface_zones_only child of auto_options.
    """
    keep_empty_interface: keep_empty_interface_cls = keep_empty_interface_cls
    """
    keep_empty_interface child of auto_options.
    """
    command_names = \
        ['naming_option']

    naming_option: naming_option_cls = naming_option_cls
    """
    naming_option command of auto_options.
    """
