#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .file_name_1 import file_name as file_name_cls
class compute_vf_only(Command):
    """
    Compute/write view factors only.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "compute-vf-only"

    argument_names = \
        ['file_name']

    file_name: file_name_cls = file_name_cls
    """
    file_name argument of compute_vf_only.
    """
