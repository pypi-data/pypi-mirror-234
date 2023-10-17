#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .phase_14 import phase as phase_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .angular import angular as angular_cls
from .p_jump import p_jump as p_jump_cls
class periodic_child(Group):
    """
    'child_object_type' of periodic.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'angular', 'p_jump']

    phase: phase_cls = phase_cls
    """
    phase child of periodic_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of periodic_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of periodic_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of periodic_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of periodic_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of periodic_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of periodic_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of periodic_child.
    """
    angular: angular_cls = angular_cls
    """
    angular child of periodic_child.
    """
    p_jump: p_jump_cls = p_jump_cls
    """
    p_jump child of periodic_child.
    """
