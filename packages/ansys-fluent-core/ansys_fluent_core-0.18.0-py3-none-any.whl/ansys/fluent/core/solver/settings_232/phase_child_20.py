#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .les_spec_name import les_spec_name as les_spec_name_cls
from .rfg_number_of_modes import rfg_number_of_modes as rfg_number_of_modes_cls
from .vm_nvortices import vm_nvortices as vm_nvortices_cls
from .les_embedded_fluctuations import les_embedded_fluctuations as les_embedded_fluctuations_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'les_spec_name',
         'rfg_number_of_modes', 'vm_nvortices', 'les_embedded_fluctuations']

    name: name_cls = name_cls
    """
    name child of phase_child.
    """
    geom_disable: geom_disable_cls = geom_disable_cls
    """
    geom_disable child of phase_child.
    """
    geom_dir_spec: geom_dir_spec_cls = geom_dir_spec_cls
    """
    geom_dir_spec child of phase_child.
    """
    geom_dir_x: geom_dir_x_cls = geom_dir_x_cls
    """
    geom_dir_x child of phase_child.
    """
    geom_dir_y: geom_dir_y_cls = geom_dir_y_cls
    """
    geom_dir_y child of phase_child.
    """
    geom_dir_z: geom_dir_z_cls = geom_dir_z_cls
    """
    geom_dir_z child of phase_child.
    """
    geom_levels: geom_levels_cls = geom_levels_cls
    """
    geom_levels child of phase_child.
    """
    geom_bgthread: geom_bgthread_cls = geom_bgthread_cls
    """
    geom_bgthread child of phase_child.
    """
    les_spec_name: les_spec_name_cls = les_spec_name_cls
    """
    les_spec_name child of phase_child.
    """
    rfg_number_of_modes: rfg_number_of_modes_cls = rfg_number_of_modes_cls
    """
    rfg_number_of_modes child of phase_child.
    """
    vm_nvortices: vm_nvortices_cls = vm_nvortices_cls
    """
    vm_nvortices child of phase_child.
    """
    les_embedded_fluctuations: les_embedded_fluctuations_cls = les_embedded_fluctuations_cls
    """
    les_embedded_fluctuations child of phase_child.
    """
