#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sc_def_file_settings import sc_def_file_settings as sc_def_file_settings_cls
from .settings import settings as settings_cls
from .abaqus import abaqus as abaqus_cls
from .mechanical_apdl import mechanical_apdl as mechanical_apdl_cls
from .mechanical_apdl_input import mechanical_apdl_input as mechanical_apdl_input_cls
from .custom_heat_flux import custom_heat_flux as custom_heat_flux_cls
from .icemcfd_for_icepak import icemcfd_for_icepak as icemcfd_for_icepak_cls
from .fast_mesh import fast_mesh as fast_mesh_cls
from .fast_solution import fast_solution as fast_solution_cls
from .fast_velocity import fast_velocity as fast_velocity_cls
from .taitherm import taitherm as taitherm_cls
class export(Group):
    """
    'export' child.
    """

    fluent_name = "export"

    child_names = \
        ['sc_def_file_settings', 'settings']

    sc_def_file_settings: sc_def_file_settings_cls = sc_def_file_settings_cls
    """
    sc_def_file_settings child of export.
    """
    settings: settings_cls = settings_cls
    """
    settings child of export.
    """
    command_names = \
        ['abaqus', 'mechanical_apdl', 'mechanical_apdl_input',
         'custom_heat_flux', 'icemcfd_for_icepak', 'fast_mesh',
         'fast_solution', 'fast_velocity', 'taitherm']

    abaqus: abaqus_cls = abaqus_cls
    """
    abaqus command of export.
    """
    mechanical_apdl: mechanical_apdl_cls = mechanical_apdl_cls
    """
    mechanical_apdl command of export.
    """
    mechanical_apdl_input: mechanical_apdl_input_cls = mechanical_apdl_input_cls
    """
    mechanical_apdl_input command of export.
    """
    custom_heat_flux: custom_heat_flux_cls = custom_heat_flux_cls
    """
    custom_heat_flux command of export.
    """
    icemcfd_for_icepak: icemcfd_for_icepak_cls = icemcfd_for_icepak_cls
    """
    icemcfd_for_icepak command of export.
    """
    fast_mesh: fast_mesh_cls = fast_mesh_cls
    """
    fast_mesh command of export.
    """
    fast_solution: fast_solution_cls = fast_solution_cls
    """
    fast_solution command of export.
    """
    fast_velocity: fast_velocity_cls = fast_velocity_cls
    """
    fast_velocity command of export.
    """
    taitherm: taitherm_cls = taitherm_cls
    """
    taitherm command of export.
    """
