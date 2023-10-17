#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .all_1 import all as all_cls
from .one_to_one_pairing import one_to_one_pairing as one_to_one_pairing_cls
from .new_si_id import new_si_id as new_si_id_cls
from .si_create import si_create as si_create_cls
from .si_name import si_name as si_name_cls
from .apply_mapped import apply_mapped as apply_mapped_cls
from .static_interface import static_interface as static_interface_cls
class auto_pairing(Command):
    """
    Automatically pair and create mesh interfaces for some or all interface zones.
    
    Parameters
    ----------
        all : bool
            'all' child.
        one_to_one_pairing : bool
            'one_to_one_pairing' child.
        new_si_id : typing.List[str]
            Select unintersected interface zones for pairing.
        si_create : bool
            'si_create' child.
        si_name : str
            Enter a prefix for mesh interface names.
        apply_mapped : bool
            Apply Mapped option at solids.
        static_interface : bool
            'static_interface' child.
    
    """

    fluent_name = "auto-pairing"

    argument_names = \
        ['all', 'one_to_one_pairing', 'new_si_id', 'si_create', 'si_name',
         'apply_mapped', 'static_interface']

    all: all_cls = all_cls
    """
    all argument of auto_pairing.
    """
    one_to_one_pairing: one_to_one_pairing_cls = one_to_one_pairing_cls
    """
    one_to_one_pairing argument of auto_pairing.
    """
    new_si_id: new_si_id_cls = new_si_id_cls
    """
    new_si_id argument of auto_pairing.
    """
    si_create: si_create_cls = si_create_cls
    """
    si_create argument of auto_pairing.
    """
    si_name: si_name_cls = si_name_cls
    """
    si_name argument of auto_pairing.
    """
    apply_mapped: apply_mapped_cls = apply_mapped_cls
    """
    apply_mapped argument of auto_pairing.
    """
    static_interface: static_interface_cls = static_interface_cls
    """
    static_interface argument of auto_pairing.
    """
