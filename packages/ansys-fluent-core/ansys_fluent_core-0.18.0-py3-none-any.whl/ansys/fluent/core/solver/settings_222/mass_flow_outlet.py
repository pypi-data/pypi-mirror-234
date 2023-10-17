#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .mass_flow_inlet_child import mass_flow_inlet_child

class mass_flow_outlet(NamedObject[mass_flow_inlet_child], _CreatableNamedObjectMixin[mass_flow_inlet_child]):
    """
    'mass_flow_outlet' child.
    """

    fluent_name = "mass-flow-outlet"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of mass_flow_outlet.
    """
    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_outlet.
    """
