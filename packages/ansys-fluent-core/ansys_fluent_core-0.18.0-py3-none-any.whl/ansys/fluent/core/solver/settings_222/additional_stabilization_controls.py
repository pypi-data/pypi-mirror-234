#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .blended_compressive_scheme import blended_compressive_scheme as blended_compressive_scheme_cls
from .pseudo_transient_stabilization import pseudo_transient_stabilization as pseudo_transient_stabilization_cls
class additional_stabilization_controls(Group):
    """
    'additional_stabilization_controls' child.
    """

    fluent_name = "additional-stabilization-controls"

    child_names = \
        ['blended_compressive_scheme', 'pseudo_transient_stabilization']

    blended_compressive_scheme: blended_compressive_scheme_cls = blended_compressive_scheme_cls
    """
    blended_compressive_scheme child of additional_stabilization_controls.
    """
    pseudo_transient_stabilization: pseudo_transient_stabilization_cls = pseudo_transient_stabilization_cls
    """
    pseudo_transient_stabilization child of additional_stabilization_controls.
    """
