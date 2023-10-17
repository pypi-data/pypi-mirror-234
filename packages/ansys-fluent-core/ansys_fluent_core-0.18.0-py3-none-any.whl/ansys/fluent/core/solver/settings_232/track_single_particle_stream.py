#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enabled_2 import enabled as enabled_cls
from .stream_id import stream_id as stream_id_cls
class track_single_particle_stream(Group):
    """
    'track_single_particle_stream' child.
    """

    fluent_name = "track-single-particle-stream"

    child_names = \
        ['enabled', 'stream_id']

    enabled: enabled_cls = enabled_cls
    """
    enabled child of track_single_particle_stream.
    """
    stream_id: stream_id_cls = stream_id_cls
    """
    stream_id child of track_single_particle_stream.
    """
