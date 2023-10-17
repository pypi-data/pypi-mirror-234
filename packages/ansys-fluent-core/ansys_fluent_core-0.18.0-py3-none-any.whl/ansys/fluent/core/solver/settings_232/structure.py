#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .model import model as model_cls
from .options_4 import options as options_cls
from .controls import controls as controls_cls
from .expert import expert as expert_cls
class structure(Group):
    """
    'structure' child.
    """

    fluent_name = "structure"

    child_names = \
        ['model', 'options', 'controls', 'expert']

    model: model_cls = model_cls
    """
    model child of structure.
    """
    options: options_cls = options_cls
    """
    options child of structure.
    """
    controls: controls_cls = controls_cls
    """
    controls child of structure.
    """
    expert: expert_cls = expert_cls
    """
    expert child of structure.
    """
