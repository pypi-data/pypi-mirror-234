#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_origin import axis_origin as axis_origin_cls
from .axis_direction import axis_direction as axis_direction_cls
from .radial_diffusivity import radial_diffusivity as radial_diffusivity_cls
from .tangential_diffusivity import tangential_diffusivity as tangential_diffusivity_cls
from .axial_diffusivity import axial_diffusivity as axial_diffusivity_cls
class cyl_orthotropic(Group):
    """
    'cyl_orthotropic' child.
    """

    fluent_name = "cyl-orthotropic"

    child_names = \
        ['axis_origin', 'axis_direction', 'radial_diffusivity',
         'tangential_diffusivity', 'axial_diffusivity']

    axis_origin: axis_origin_cls = axis_origin_cls
    """
    axis_origin child of cyl_orthotropic.
    """
    axis_direction: axis_direction_cls = axis_direction_cls
    """
    axis_direction child of cyl_orthotropic.
    """
    radial_diffusivity: radial_diffusivity_cls = radial_diffusivity_cls
    """
    radial_diffusivity child of cyl_orthotropic.
    """
    tangential_diffusivity: tangential_diffusivity_cls = tangential_diffusivity_cls
    """
    tangential_diffusivity child of cyl_orthotropic.
    """
    axial_diffusivity: axial_diffusivity_cls = axial_diffusivity_cls
    """
    axial_diffusivity child of cyl_orthotropic.
    """
