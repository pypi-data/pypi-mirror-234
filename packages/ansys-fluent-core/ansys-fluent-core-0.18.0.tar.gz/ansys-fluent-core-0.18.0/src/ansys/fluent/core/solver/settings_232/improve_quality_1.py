#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .check_mapped_interface_quality import check_mapped_interface_quality as check_mapped_interface_quality_cls
from .complete import complete as complete_cls
from .tol_percentage_increment import tol_percentage_increment as tol_percentage_increment_cls
class improve_quality(Command):
    """
    Improve mesh interface quality.
    
    Parameters
    ----------
        check_mapped_interface_quality : bool
            Check Mapped Interface Qaulity.
        complete : bool
            Continue to improve the mapped interface quality.
        tol_percentage_increment : real
            'tol_percentage_increment' child.
    
    """

    fluent_name = "improve-quality"

    argument_names = \
        ['check_mapped_interface_quality', 'complete',
         'tol_percentage_increment']

    check_mapped_interface_quality: check_mapped_interface_quality_cls = check_mapped_interface_quality_cls
    """
    check_mapped_interface_quality argument of improve_quality.
    """
    complete: complete_cls = complete_cls
    """
    complete argument of improve_quality.
    """
    tol_percentage_increment: tol_percentage_increment_cls = tol_percentage_increment_cls
    """
    tol_percentage_increment argument of improve_quality.
    """
