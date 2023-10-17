#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_10 import option as option_cls
from .diffusion_controlled import diffusion_controlled as diffusion_controlled_cls
from .convection_diffusion_controlled import convection_diffusion_controlled as convection_diffusion_controlled_cls
class vaporization_model(Group):
    """
    'vaporization_model' child.
    """

    fluent_name = "vaporization-model"

    child_names = \
        ['option', 'diffusion_controlled', 'convection_diffusion_controlled']

    option: option_cls = option_cls
    """
    option child of vaporization_model.
    """
    diffusion_controlled: diffusion_controlled_cls = diffusion_controlled_cls
    """
    diffusion_controlled child of vaporization_model.
    """
    convection_diffusion_controlled: convection_diffusion_controlled_cls = convection_diffusion_controlled_cls
    """
    convection_diffusion_controlled child of vaporization_model.
    """
