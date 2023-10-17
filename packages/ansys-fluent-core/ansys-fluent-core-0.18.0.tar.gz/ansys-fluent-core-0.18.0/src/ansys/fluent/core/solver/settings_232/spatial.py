#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .first_to_second_order_blending_1 import first_to_second_order_blending as first_to_second_order_blending_cls
from .first_to_second_order_blending_list import first_to_second_order_blending_list as first_to_second_order_blending_list_cls
from .scheme_1 import scheme as scheme_cls
from .flow_skew_diffusion_exclude import flow_skew_diffusion_exclude as flow_skew_diffusion_exclude_cls
from .scalars_skew_diffusion_exclude import scalars_skew_diffusion_exclude as scalars_skew_diffusion_exclude_cls
from .rhie_chow_flux_specify import rhie_chow_flux_specify as rhie_chow_flux_specify_cls
from .rhie_chow_method import rhie_chow_method as rhie_chow_method_cls
class spatial(Group):
    """
    'spatial' child.
    """

    fluent_name = "spatial"

    child_names = \
        ['first_to_second_order_blending',
         'first_to_second_order_blending_list', 'scheme',
         'flow_skew_diffusion_exclude', 'scalars_skew_diffusion_exclude',
         'rhie_chow_flux_specify', 'rhie_chow_method']

    first_to_second_order_blending: first_to_second_order_blending_cls = first_to_second_order_blending_cls
    """
    first_to_second_order_blending child of spatial.
    """
    first_to_second_order_blending_list: first_to_second_order_blending_list_cls = first_to_second_order_blending_list_cls
    """
    first_to_second_order_blending_list child of spatial.
    """
    scheme: scheme_cls = scheme_cls
    """
    scheme child of spatial.
    """
    flow_skew_diffusion_exclude: flow_skew_diffusion_exclude_cls = flow_skew_diffusion_exclude_cls
    """
    flow_skew_diffusion_exclude child of spatial.
    """
    scalars_skew_diffusion_exclude: scalars_skew_diffusion_exclude_cls = scalars_skew_diffusion_exclude_cls
    """
    scalars_skew_diffusion_exclude child of spatial.
    """
    rhie_chow_flux_specify: rhie_chow_flux_specify_cls = rhie_chow_flux_specify_cls
    """
    rhie_chow_flux_specify child of spatial.
    """
    rhie_chow_method: rhie_chow_method_cls = rhie_chow_method_cls
    """
    rhie_chow_method child of spatial.
    """
