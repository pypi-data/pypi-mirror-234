#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .wall_distance_free import wall_distance_free as wall_distance_free_cls
from .cjet import cjet as cjet_cls
from .creal import creal as creal_cls
from .cnw_sub import cnw_sub as cnw_sub_cls
from .cjet_aux import cjet_aux as cjet_aux_cls
from .cbf_lam import cbf_lam as cbf_lam_cls
from .cbf_tur import cbf_tur as cbf_tur_cls
from .geko_defaults import geko_defaults as geko_defaults_cls
class geko_options(Group):
    """
    'geko_options' child.
    """

    fluent_name = "geko-options"

    child_names = \
        ['wall_distance_free', 'cjet', 'creal', 'cnw_sub', 'cjet_aux',
         'cbf_lam', 'cbf_tur']

    wall_distance_free: wall_distance_free_cls = wall_distance_free_cls
    """
    wall_distance_free child of geko_options.
    """
    cjet: cjet_cls = cjet_cls
    """
    cjet child of geko_options.
    """
    creal: creal_cls = creal_cls
    """
    creal child of geko_options.
    """
    cnw_sub: cnw_sub_cls = cnw_sub_cls
    """
    cnw_sub child of geko_options.
    """
    cjet_aux: cjet_aux_cls = cjet_aux_cls
    """
    cjet_aux child of geko_options.
    """
    cbf_lam: cbf_lam_cls = cbf_lam_cls
    """
    cbf_lam child of geko_options.
    """
    cbf_tur: cbf_tur_cls = cbf_tur_cls
    """
    cbf_tur child of geko_options.
    """
    command_names = \
        ['geko_defaults']

    geko_defaults: geko_defaults_cls = geko_defaults_cls
    """
    geko_defaults command of geko_options.
    """
