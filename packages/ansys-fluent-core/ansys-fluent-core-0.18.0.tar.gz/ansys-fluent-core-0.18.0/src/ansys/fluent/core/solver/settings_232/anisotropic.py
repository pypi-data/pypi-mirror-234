#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .matrix_component import matrix_component as matrix_component_cls
from .diffusivity import diffusivity as diffusivity_cls
class anisotropic(Group):
    """
    'anisotropic' child.
    """

    fluent_name = "anisotropic"

    child_names = \
        ['matrix_component', 'diffusivity']

    matrix_component: matrix_component_cls = matrix_component_cls
    """
    matrix_component child of anisotropic.
    """
    diffusivity: diffusivity_cls = diffusivity_cls
    """
    diffusivity child of anisotropic.
    """
