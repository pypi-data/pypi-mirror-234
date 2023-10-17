#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .zone_name import zone_name as zone_name_cls
from .overwrite import overwrite as overwrite_cls
class copy_mesh_to_mrf_motion(Command):
    """
    Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.
    
    Parameters
    ----------
        zone_name : str
            'zone_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "copy-mesh-to-mrf-motion"

    argument_names = \
        ['zone_name', 'overwrite']

    zone_name: zone_name_cls = zone_name_cls
    """
    zone_name argument of copy_mesh_to_mrf_motion.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of copy_mesh_to_mrf_motion.
    """
