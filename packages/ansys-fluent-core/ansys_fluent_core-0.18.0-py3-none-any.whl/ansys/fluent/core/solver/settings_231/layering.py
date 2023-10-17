#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .use_layering import use_layering as use_layering_cls
from .base_face_zone_for_partitioning import base_face_zone_for_partitioning as base_face_zone_for_partitioning_cls
class layering(Group):
    """
    Use layering for partitioning.
    """

    fluent_name = "layering"

    child_names = \
        ['use_layering', 'base_face_zone_for_partitioning']

    use_layering: use_layering_cls = use_layering_cls
    """
    use_layering child of layering.
    """
    base_face_zone_for_partitioning: base_face_zone_for_partitioning_cls = base_face_zone_for_partitioning_cls
    """
    base_face_zone_for_partitioning child of layering.
    """
