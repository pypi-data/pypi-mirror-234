#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .planar_conductivity import planar_conductivity as planar_conductivity_cls
from .transverse_conductivity import transverse_conductivity as transverse_conductivity_cls
class biaxial(Group):
    """
    'biaxial' child.
    """

    fluent_name = "biaxial"

    child_names = \
        ['planar_conductivity', 'transverse_conductivity']

    planar_conductivity: planar_conductivity_cls = planar_conductivity_cls
    """
    planar_conductivity child of biaxial.
    """
    transverse_conductivity: transverse_conductivity_cls = transverse_conductivity_cls
    """
    transverse_conductivity child of biaxial.
    """
