#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .thickness import thickness as thickness_cls
from .material import material as material_cls
from .qdot import qdot as qdot_cls
class shell_conduction_child(Group):
    """
    'child_object_type' of shell_conduction.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['thickness', 'material', 'qdot']

    thickness: thickness_cls = thickness_cls
    """
    thickness child of shell_conduction_child.
    """
    material: material_cls = material_cls
    """
    material child of shell_conduction_child.
    """
    qdot: qdot_cls = qdot_cls
    """
    qdot child of shell_conduction_child.
    """
