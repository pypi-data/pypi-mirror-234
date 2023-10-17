#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .averaging_coefficient import averaging_coefficient as averaging_coefficient_cls
from .binary_diffusivity import binary_diffusivity as binary_diffusivity_cls
class film_averaged(Group):
    """
    'film_averaged' child.
    """

    fluent_name = "film-averaged"

    child_names = \
        ['averaging_coefficient', 'binary_diffusivity']

    averaging_coefficient: averaging_coefficient_cls = averaging_coefficient_cls
    """
    averaging_coefficient child of film_averaged.
    """
    binary_diffusivity: binary_diffusivity_cls = binary_diffusivity_cls
    """
    binary_diffusivity child of film_averaged.
    """
