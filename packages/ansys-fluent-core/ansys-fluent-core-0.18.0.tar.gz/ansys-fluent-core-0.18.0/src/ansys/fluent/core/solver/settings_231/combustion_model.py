#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_9 import option as option_cls
from .cbk import cbk as cbk_cls
from .kinetics_diffusion_limited import kinetics_diffusion_limited as kinetics_diffusion_limited_cls
from .intrinsic_model import intrinsic_model as intrinsic_model_cls
from .multiple_surface_reactions import multiple_surface_reactions as multiple_surface_reactions_cls
class combustion_model(Group):
    """
    'combustion_model' child.
    """

    fluent_name = "combustion-model"

    child_names = \
        ['option', 'cbk', 'kinetics_diffusion_limited', 'intrinsic_model',
         'multiple_surface_reactions']

    option: option_cls = option_cls
    """
    option child of combustion_model.
    """
    cbk: cbk_cls = cbk_cls
    """
    cbk child of combustion_model.
    """
    kinetics_diffusion_limited: kinetics_diffusion_limited_cls = kinetics_diffusion_limited_cls
    """
    kinetics_diffusion_limited child of combustion_model.
    """
    intrinsic_model: intrinsic_model_cls = intrinsic_model_cls
    """
    intrinsic_model child of combustion_model.
    """
    multiple_surface_reactions: multiple_surface_reactions_cls = multiple_surface_reactions_cls
    """
    multiple_surface_reactions child of combustion_model.
    """
