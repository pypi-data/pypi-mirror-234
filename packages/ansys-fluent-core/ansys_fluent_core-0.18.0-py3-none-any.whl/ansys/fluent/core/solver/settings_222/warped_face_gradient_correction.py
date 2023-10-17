#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_3 import enable as enable_cls
from .turbulence_options import turbulence_options as turbulence_options_cls
class warped_face_gradient_correction(Group):
    """
    'warped_face_gradient_correction' child.
    """

    fluent_name = "warped-face-gradient-correction"

    child_names = \
        ['enable', 'turbulence_options']

    enable: enable_cls = enable_cls
    """
    enable child of warped_face_gradient_correction.
    """
    turbulence_options: turbulence_options_cls = turbulence_options_cls
    """
    turbulence_options child of warped_face_gradient_correction.
    """
