#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name_1 import name as name_cls
from .animate_on import animate_on as animate_on_cls
from .frequency_1 import frequency as frequency_cls
from .flow_time_frequency import flow_time_frequency as flow_time_frequency_cls
from .frequency_of import frequency_of as frequency_of_cls
from .storage_type import storage_type as storage_type_cls
from .storage_dir import storage_dir as storage_dir_cls
from .window_id import window_id as window_id_cls
from .view import view as view_cls
from .use_raytracing import use_raytracing as use_raytracing_cls
from .display_3 import display as display_cls
class solution_animations_child(Group):
    """
    'child_object_type' of solution_animations.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'animate_on', 'frequency', 'flow_time_frequency',
         'frequency_of', 'storage_type', 'storage_dir', 'window_id', 'view',
         'use_raytracing']

    name: name_cls = name_cls
    """
    name child of solution_animations_child.
    """
    animate_on: animate_on_cls = animate_on_cls
    """
    animate_on child of solution_animations_child.
    """
    frequency: frequency_cls = frequency_cls
    """
    frequency child of solution_animations_child.
    """
    flow_time_frequency: flow_time_frequency_cls = flow_time_frequency_cls
    """
    flow_time_frequency child of solution_animations_child.
    """
    frequency_of: frequency_of_cls = frequency_of_cls
    """
    frequency_of child of solution_animations_child.
    """
    storage_type: storage_type_cls = storage_type_cls
    """
    storage_type child of solution_animations_child.
    """
    storage_dir: storage_dir_cls = storage_dir_cls
    """
    storage_dir child of solution_animations_child.
    """
    window_id: window_id_cls = window_id_cls
    """
    window_id child of solution_animations_child.
    """
    view: view_cls = view_cls
    """
    view child of solution_animations_child.
    """
    use_raytracing: use_raytracing_cls = use_raytracing_cls
    """
    use_raytracing child of solution_animations_child.
    """
    command_names = \
        ['display']

    display: display_cls = display_cls
    """
    display command of solution_animations_child.
    """
