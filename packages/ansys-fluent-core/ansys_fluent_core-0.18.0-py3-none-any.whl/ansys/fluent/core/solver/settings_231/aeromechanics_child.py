#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_type import report_type as report_type_cls
from .realcomponent import realcomponent as realcomponent_cls
from .nodal_diameters import nodal_diameters as nodal_diameters_cls
from .normalization import normalization as normalization_cls
from .integrate_over import integrate_over as integrate_over_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .old_props import old_props as old_props_cls
from .thread_names import thread_names as thread_names_cls
from .thread_ids import thread_ids as thread_ids_cls
class aeromechanics_child(Group):
    """
    'child_object_type' of aeromechanics.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['report_type', 'realcomponent', 'nodal_diameters', 'normalization',
         'integrate_over', 'average_over', 'per_zone', 'old_props',
         'thread_names', 'thread_ids']

    report_type: report_type_cls = report_type_cls
    """
    report_type child of aeromechanics_child.
    """
    realcomponent: realcomponent_cls = realcomponent_cls
    """
    realcomponent child of aeromechanics_child.
    """
    nodal_diameters: nodal_diameters_cls = nodal_diameters_cls
    """
    nodal_diameters child of aeromechanics_child.
    """
    normalization: normalization_cls = normalization_cls
    """
    normalization child of aeromechanics_child.
    """
    integrate_over: integrate_over_cls = integrate_over_cls
    """
    integrate_over child of aeromechanics_child.
    """
    average_over: average_over_cls = average_over_cls
    """
    average_over child of aeromechanics_child.
    """
    per_zone: per_zone_cls = per_zone_cls
    """
    per_zone child of aeromechanics_child.
    """
    old_props: old_props_cls = old_props_cls
    """
    old_props child of aeromechanics_child.
    """
    thread_names: thread_names_cls = thread_names_cls
    """
    thread_names child of aeromechanics_child.
    """
    thread_ids: thread_ids_cls = thread_ids_cls
    """
    thread_ids child of aeromechanics_child.
    """
