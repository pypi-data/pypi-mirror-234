#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .pole_real import pole_real as pole_real_cls
from .pole_imag import pole_imag as pole_imag_cls
from .amplitude_real import amplitude_real as amplitude_real_cls
from .amplitude_imag import amplitude_imag as amplitude_imag_cls
class impedance_2_child(Group):
    """
    'child_object_type' of impedance_2.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pole_real', 'pole_imag', 'amplitude_real', 'amplitude_imag']

    pole_real: pole_real_cls = pole_real_cls
    """
    pole_real child of impedance_2_child.
    """
    pole_imag: pole_imag_cls = pole_imag_cls
    """
    pole_imag child of impedance_2_child.
    """
    amplitude_real: amplitude_real_cls = amplitude_real_cls
    """
    amplitude_real child of impedance_2_child.
    """
    amplitude_imag: amplitude_imag_cls = amplitude_imag_cls
    """
    amplitude_imag child of impedance_2_child.
    """
