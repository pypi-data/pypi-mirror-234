#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .blended_compressive_scheme import blended_compressive_scheme as blended_compressive_scheme_cls
from .pseudo_time_stabilization import pseudo_time_stabilization as pseudo_time_stabilization_cls
class additional_stabilization_controls(Group):
    """
    Additional advanced stability controls for VOF.
    """

    fluent_name = "additional-stabilization-controls"

    child_names = \
        ['blended_compressive_scheme', 'pseudo_time_stabilization']

    blended_compressive_scheme: blended_compressive_scheme_cls = blended_compressive_scheme_cls
    """
    blended_compressive_scheme child of additional_stabilization_controls.
    """
    pseudo_time_stabilization: pseudo_time_stabilization_cls = pseudo_time_stabilization_cls
    """
    pseudo_time_stabilization child of additional_stabilization_controls.
    """
