#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .verbosity_6 import verbosity as verbosity_cls
from .skewness_neighbor_coupling import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .hybrid_nita_settings import hybrid_nita_settings as hybrid_nita_settings_cls
class nita_expert_controls(Group):
    """
    Enter the nita expert controls menu.
    """

    fluent_name = "nita-expert-controls"

    child_names = \
        ['verbosity', 'skewness_neighbor_coupling', 'hybrid_nita_settings']

    verbosity: verbosity_cls = verbosity_cls
    """
    verbosity child of nita_expert_controls.
    """
    skewness_neighbor_coupling: skewness_neighbor_coupling_cls = skewness_neighbor_coupling_cls
    """
    skewness_neighbor_coupling child of nita_expert_controls.
    """
    hybrid_nita_settings: hybrid_nita_settings_cls = hybrid_nita_settings_cls
    """
    hybrid_nita_settings child of nita_expert_controls.
    """
