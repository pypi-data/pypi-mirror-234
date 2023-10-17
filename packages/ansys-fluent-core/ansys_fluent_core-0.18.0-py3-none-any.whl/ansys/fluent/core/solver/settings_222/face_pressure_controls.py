#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .face_pressure_options import face_pressure_options as face_pressure_options_cls
class face_pressure_controls(Group):
    """
    'face_pressure_controls' child.
    """

    fluent_name = "face-pressure-controls"

    child_names = \
        ['face_pressure_options']

    face_pressure_options: face_pressure_options_cls = face_pressure_options_cls
    """
    face_pressure_options child of face_pressure_controls.
    """
