#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .particle_type import particle_type as particle_type_cls
from .material import material as material_cls
from .reference_frame import reference_frame as reference_frame_cls
from .number_of_streams import number_of_streams as number_of_streams_cls
from .injection_type import injection_type as injection_type_cls
from .interaction_1 import interaction as interaction_cls
from .parcel_method import parcel_method as parcel_method_cls
from .particle_reinjector import particle_reinjector as particle_reinjector_cls
from .physical_models import physical_models as physical_models_cls
from .initial_props import initial_props as initial_props_cls
class injections_child(Group):
    """
    'child_object_type' of injections.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['particle_type', 'material', 'reference_frame', 'number_of_streams',
         'injection_type', 'interaction', 'parcel_method',
         'particle_reinjector', 'physical_models', 'initial_props']

    particle_type: particle_type_cls = particle_type_cls
    """
    particle_type child of injections_child.
    """
    material: material_cls = material_cls
    """
    material child of injections_child.
    """
    reference_frame: reference_frame_cls = reference_frame_cls
    """
    reference_frame child of injections_child.
    """
    number_of_streams: number_of_streams_cls = number_of_streams_cls
    """
    number_of_streams child of injections_child.
    """
    injection_type: injection_type_cls = injection_type_cls
    """
    injection_type child of injections_child.
    """
    interaction: interaction_cls = interaction_cls
    """
    interaction child of injections_child.
    """
    parcel_method: parcel_method_cls = parcel_method_cls
    """
    parcel_method child of injections_child.
    """
    particle_reinjector: particle_reinjector_cls = particle_reinjector_cls
    """
    particle_reinjector child of injections_child.
    """
    physical_models: physical_models_cls = physical_models_cls
    """
    physical_models child of injections_child.
    """
    initial_props: initial_props_cls = initial_props_cls
    """
    initial_props child of injections_child.
    """
