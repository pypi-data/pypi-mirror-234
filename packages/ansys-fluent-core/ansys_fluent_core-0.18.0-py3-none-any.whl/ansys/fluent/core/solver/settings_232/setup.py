#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .general import general as general_cls
from .models_1 import models as models_cls
from .materials import materials as materials_cls
from .cell_zone_conditions import cell_zone_conditions as cell_zone_conditions_cls
from .boundary_conditions import boundary_conditions as boundary_conditions_cls
from .reference_values import reference_values as reference_values_cls
from .named_expressions import named_expressions as named_expressions_cls
from .mesh_interfaces import mesh_interfaces as mesh_interfaces_cls
from .geometry_3 import geometry as geometry_cls
from .physics import physics as physics_cls
from .reference_frames import reference_frames as reference_frames_cls
class setup(Group):
    """
    'setup' child.
    """

    fluent_name = "setup"

    child_names = \
        ['general', 'models', 'materials', 'cell_zone_conditions',
         'boundary_conditions', 'reference_values', 'named_expressions',
         'mesh_interfaces', 'geometry', 'physics', 'reference_frames']

    general: general_cls = general_cls
    """
    general child of setup.
    """
    models: models_cls = models_cls
    """
    models child of setup.
    """
    materials: materials_cls = materials_cls
    """
    materials child of setup.
    """
    cell_zone_conditions: cell_zone_conditions_cls = cell_zone_conditions_cls
    """
    cell_zone_conditions child of setup.
    """
    boundary_conditions: boundary_conditions_cls = boundary_conditions_cls
    """
    boundary_conditions child of setup.
    """
    reference_values: reference_values_cls = reference_values_cls
    """
    reference_values child of setup.
    """
    named_expressions: named_expressions_cls = named_expressions_cls
    """
    named_expressions child of setup.
    """
    mesh_interfaces: mesh_interfaces_cls = mesh_interfaces_cls
    """
    mesh_interfaces child of setup.
    """
    geometry: geometry_cls = geometry_cls
    """
    geometry child of setup.
    """
    physics: physics_cls = physics_cls
    """
    physics child of setup.
    """
    reference_frames: reference_frames_cls = reference_frames_cls
    """
    reference_frames child of setup.
    """
