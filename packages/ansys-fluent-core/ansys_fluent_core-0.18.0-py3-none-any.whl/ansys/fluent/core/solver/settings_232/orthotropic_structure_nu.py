#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .poisson_ratio_01 import poisson_ratio_01 as poisson_ratio_01_cls
from .poisson_ratio_12 import poisson_ratio_12 as poisson_ratio_12_cls
from .poisson_ratio_02 import poisson_ratio_02 as poisson_ratio_02_cls
class orthotropic_structure_nu(Group):
    """
    'orthotropic_structure_nu' child.
    """

    fluent_name = "orthotropic-structure-nu"

    child_names = \
        ['poisson_ratio_01', 'poisson_ratio_12', 'poisson_ratio_02']

    poisson_ratio_01: poisson_ratio_01_cls = poisson_ratio_01_cls
    """
    poisson_ratio_01 child of orthotropic_structure_nu.
    """
    poisson_ratio_12: poisson_ratio_12_cls = poisson_ratio_12_cls
    """
    poisson_ratio_12 child of orthotropic_structure_nu.
    """
    poisson_ratio_02: poisson_ratio_02_cls = poisson_ratio_02_cls
    """
    poisson_ratio_02 child of orthotropic_structure_nu.
    """
