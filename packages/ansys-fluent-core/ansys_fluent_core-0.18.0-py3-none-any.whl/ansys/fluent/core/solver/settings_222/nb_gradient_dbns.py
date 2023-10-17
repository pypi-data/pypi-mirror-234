#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .boundary_treatment import boundary_treatment as boundary_treatment_cls
from .extended_boundary_treatment import extended_boundary_treatment as extended_boundary_treatment_cls
class nb_gradient_dbns(Group):
    """
    'nb_gradient_dbns' child.
    """

    fluent_name = "nb-gradient-dbns"

    child_names = \
        ['boundary_treatment', 'extended_boundary_treatment']

    boundary_treatment: boundary_treatment_cls = boundary_treatment_cls
    """
    boundary_treatment child of nb_gradient_dbns.
    """
    extended_boundary_treatment: extended_boundary_treatment_cls = extended_boundary_treatment_cls
    """
    extended_boundary_treatment child of nb_gradient_dbns.
    """
