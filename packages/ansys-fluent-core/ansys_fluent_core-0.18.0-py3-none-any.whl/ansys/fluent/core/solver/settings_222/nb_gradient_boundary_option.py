#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .nb_gradient import nb_gradient as nb_gradient_cls
from .nb_gradient_dbns import nb_gradient_dbns as nb_gradient_dbns_cls
class nb_gradient_boundary_option(Group):
    """
    'nb_gradient_boundary_option' child.
    """

    fluent_name = "nb-gradient-boundary-option?"

    child_names = \
        ['nb_gradient', 'nb_gradient_dbns']

    nb_gradient: nb_gradient_cls = nb_gradient_cls
    """
    nb_gradient child of nb_gradient_boundary_option.
    """
    nb_gradient_dbns: nb_gradient_dbns_cls = nb_gradient_dbns_cls
    """
    nb_gradient_dbns child of nb_gradient_boundary_option.
    """
