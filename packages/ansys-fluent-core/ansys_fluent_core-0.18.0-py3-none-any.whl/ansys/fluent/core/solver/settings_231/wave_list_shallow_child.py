#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .theory import theory as theory_cls
from .wave_ht import wave_ht as wave_ht_cls
from .wave_len import wave_len as wave_len_cls
from .offset_1 import offset as offset_cls
from .heading_angle import heading_angle as heading_angle_cls
class wave_list_shallow_child(Group):
    """
    'child_object_type' of wave_list_shallow.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['theory', 'wave_ht', 'wave_len', 'offset', 'heading_angle']

    theory: theory_cls = theory_cls
    """
    theory child of wave_list_shallow_child.
    """
    wave_ht: wave_ht_cls = wave_ht_cls
    """
    wave_ht child of wave_list_shallow_child.
    """
    wave_len: wave_len_cls = wave_len_cls
    """
    wave_len child of wave_list_shallow_child.
    """
    offset: offset_cls = offset_cls
    """
    offset child of wave_list_shallow_child.
    """
    heading_angle: heading_angle_cls = heading_angle_cls
    """
    heading_angle child of wave_list_shallow_child.
    """
