#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .from_zone_type import from_zone_type as from_zone_type_cls
from .from_zone_name import from_zone_name as from_zone_name_cls
from .phase_25 import phase as phase_cls
class compute_defaults(Command):
    """
    'compute_defaults' command.
    
    Parameters
    ----------
        from_zone_type : str
            'from_zone_type' child.
        from_zone_name : str
            'from_zone_name' child.
        phase : str
            'phase' child.
    
    """

    fluent_name = "compute-defaults"

    argument_names = \
        ['from_zone_type', 'from_zone_name', 'phase']

    from_zone_type: from_zone_type_cls = from_zone_type_cls
    """
    from_zone_type argument of compute_defaults.
    """
    from_zone_name: from_zone_name_cls = from_zone_name_cls
    """
    from_zone_name argument of compute_defaults.
    """
    phase: phase_cls = phase_cls
    """
    phase argument of compute_defaults.
    """
