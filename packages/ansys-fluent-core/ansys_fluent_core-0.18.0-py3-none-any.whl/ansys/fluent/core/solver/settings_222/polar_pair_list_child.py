#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .polar_real_angle import polar_real_angle as polar_real_angle_cls
from .polar_real_intensity import polar_real_intensity as polar_real_intensity_cls
class polar_pair_list_child(Group):
    """
    'child_object_type' of polar_pair_list.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['polar_real_angle', 'polar_real_intensity']

    polar_real_angle: polar_real_angle_cls = polar_real_angle_cls
    """
    polar_real_angle child of polar_pair_list_child.
    """
    polar_real_intensity: polar_real_intensity_cls = polar_real_intensity_cls
    """
    polar_real_intensity child of polar_pair_list_child.
    """
