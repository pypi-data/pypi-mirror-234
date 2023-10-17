#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .change_type import change_type as change_type_cls
from .recirculation_inlet_child import recirculation_inlet_child

class recirculation_inlet(NamedObject[recirculation_inlet_child], _CreatableNamedObjectMixin[recirculation_inlet_child]):
    """
    'recirculation_inlet' child.
    """

    fluent_name = "recirculation-inlet"

    command_names = \
        ['change_type']

    change_type: change_type_cls = change_type_cls
    """
    change_type command of recirculation_inlet.
    """
    child_object_type: recirculation_inlet_child = recirculation_inlet_child
    """
    child_object_type of recirculation_inlet.
    """
