#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .filename import filename as filename_cls
from .unit import unit as unit_cls
class read(Command):
    """
    Read surface meshes.
    
    Parameters
    ----------
        filename : str
            'filename' child.
        unit : str
            'unit' child.
    
    """

    fluent_name = "read"

    argument_names = \
        ['filename', 'unit']

    filename: filename_cls = filename_cls
    """
    filename argument of read.
    """
    unit: unit_cls = unit_cls
    """
    unit argument of read.
    """
