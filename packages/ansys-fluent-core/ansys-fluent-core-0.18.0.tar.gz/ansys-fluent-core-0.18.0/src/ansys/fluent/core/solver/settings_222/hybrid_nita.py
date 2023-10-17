#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .outer_iterations import outer_iterations as outer_iterations_cls
from .initial_outer_iterations import initial_outer_iterations as initial_outer_iterations_cls
from .instability_detector import instability_detector as instability_detector_cls
class hybrid_nita(Group):
    """
    'hybrid_nita' child.
    """

    fluent_name = "hybrid-nita"

    child_names = \
        ['outer_iterations', 'initial_outer_iterations',
         'instability_detector']

    outer_iterations: outer_iterations_cls = outer_iterations_cls
    """
    outer_iterations child of hybrid_nita.
    """
    initial_outer_iterations: initial_outer_iterations_cls = initial_outer_iterations_cls
    """
    initial_outer_iterations child of hybrid_nita.
    """
    instability_detector: instability_detector_cls = instability_detector_cls
    """
    instability_detector child of hybrid_nita.
    """
