#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .mf_1 import mf as mf_cls
from .urf import urf as urf_cls
class solution_controls(Command):
    """
    Specification of mapped frequency and under-relaxation factor for mapped interfaces.
    
    Parameters
    ----------
        mf : int
            'mf' child.
        urf : real
            'urf' child.
    
    """

    fluent_name = "solution-controls"

    argument_names = \
        ['mf', 'urf']

    mf: mf_cls = mf_cls
    """
    mf argument of solution_controls.
    """
    urf: urf_cls = urf_cls
    """
    urf argument of solution_controls.
    """
