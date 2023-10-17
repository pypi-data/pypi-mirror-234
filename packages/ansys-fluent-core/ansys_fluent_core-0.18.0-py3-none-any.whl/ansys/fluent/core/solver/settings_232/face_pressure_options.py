#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pressure_corr_grad import pressure_corr_grad as pressure_corr_grad_cls
from .face_pressure_calculation_method import face_pressure_calculation_method as face_pressure_calculation_method_cls
from .exclude_transient_term_in_face_pressure_calc import exclude_transient_term_in_face_pressure_calc as exclude_transient_term_in_face_pressure_calc_cls
class face_pressure_options(Group):
    """
    Set face pressure options.
    """

    fluent_name = "face-pressure-options"

    child_names = \
        ['pressure_corr_grad', 'face_pressure_calculation_method',
         'exclude_transient_term_in_face_pressure_calc']

    pressure_corr_grad: pressure_corr_grad_cls = pressure_corr_grad_cls
    """
    pressure_corr_grad child of face_pressure_options.
    """
    face_pressure_calculation_method: face_pressure_calculation_method_cls = face_pressure_calculation_method_cls
    """
    face_pressure_calculation_method child of face_pressure_options.
    """
    exclude_transient_term_in_face_pressure_calc: exclude_transient_term_in_face_pressure_calc_cls = exclude_transient_term_in_face_pressure_calc_cls
    """
    exclude_transient_term_in_face_pressure_calc child of face_pressure_options.
    """
