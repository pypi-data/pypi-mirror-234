#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .sbes_sdes_hybrid_model_optn import sbes_sdes_hybrid_model_optn as sbes_sdes_hybrid_model_optn_cls
from .user_defined_1 import user_defined as user_defined_cls
class sbes_sdes_hybrid_model(Group):
    """
    'sbes_sdes_hybrid_model' child.
    """

    fluent_name = "sbes-sdes-hybrid-model"

    child_names = \
        ['sbes_sdes_hybrid_model_optn', 'user_defined']

    sbes_sdes_hybrid_model_optn: sbes_sdes_hybrid_model_optn_cls = sbes_sdes_hybrid_model_optn_cls
    """
    sbes_sdes_hybrid_model_optn child of sbes_sdes_hybrid_model.
    """
    user_defined: user_defined_cls = user_defined_cls
    """
    user_defined child of sbes_sdes_hybrid_model.
    """
