#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .o2o_flag import o2o_flag as o2o_flag_cls
from .toggle import toggle as toggle_cls
from .delete_empty import delete_empty as delete_empty_cls
class enable_one_to_one_pairing(Command):
    """
    Use the default one-to-one interface creation method?.
    
    Parameters
    ----------
        o2o_flag : bool
            Use the default one-to-one interface creation method?.
        toggle : bool
            Would you like to proceed?.
        delete_empty : bool
            Delete empty interface interior zones from non-overlapping interfaces?.
    
    """

    fluent_name = "enable-one-to-one-pairing"

    argument_names = \
        ['o2o_flag', 'toggle', 'delete_empty']

    o2o_flag: o2o_flag_cls = o2o_flag_cls
    """
    o2o_flag argument of enable_one_to_one_pairing.
    """
    toggle: toggle_cls = toggle_cls
    """
    toggle argument of enable_one_to_one_pairing.
    """
    delete_empty: delete_empty_cls = delete_empty_cls
    """
    delete_empty argument of enable_one_to_one_pairing.
    """
