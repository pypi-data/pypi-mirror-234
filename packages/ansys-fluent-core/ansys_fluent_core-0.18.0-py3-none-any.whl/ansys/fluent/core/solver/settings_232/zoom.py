#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .factor import factor as factor_cls
class zoom(Command):
    """
    Adjust the camera field of view.
    
    Parameters
    ----------
        factor : real
            'factor' child.
    
    """

    fluent_name = "zoom"

    argument_names = \
        ['factor']

    factor: factor_cls = factor_cls
    """
    factor argument of zoom.
    """
