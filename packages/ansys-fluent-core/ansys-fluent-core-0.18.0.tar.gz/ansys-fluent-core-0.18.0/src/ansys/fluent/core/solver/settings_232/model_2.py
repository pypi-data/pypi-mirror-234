#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option import option as option_cls
from .material import material as material_cls
from .phase_material import phase_material as phase_material_cls
class model(Group):
    """
    'model' child.
    """

    fluent_name = "model"

    child_names = \
        ['option', 'material', 'phase_material']

    option: option_cls = option_cls
    """
    option child of model.
    """
    material: material_cls = material_cls
    """
    material child of model.
    """
    phase_material: phase_material_cls = phase_material_cls
    """
    phase_material child of model.
    """
