#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .radius_ratio import radius_ratio as radius_ratio_cls
from .chord import chord as chord_cls
from .twist import twist as twist_cls
from .airfoil_data_file import airfoil_data_file as airfoil_data_file_cls
class geometry_child(Group):
    """
    'child_object_type' of geometry.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['radius_ratio', 'chord', 'twist', 'airfoil_data_file']

    radius_ratio: radius_ratio_cls = radius_ratio_cls
    """
    radius_ratio child of geometry_child.
    """
    chord: chord_cls = chord_cls
    """
    chord child of geometry_child.
    """
    twist: twist_cls = twist_cls
    """
    twist child of geometry_child.
    """
    airfoil_data_file: airfoil_data_file_cls = airfoil_data_file_cls
    """
    airfoil_data_file child of geometry_child.
    """
