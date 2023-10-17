#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .check_reduction_wt import check_reduction_wt as check_reduction_wt_cls
from .file_name_1 import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls
class reduce_picked_sample(Command):
    """
    Reduce a sample after first picking it and setting up all data-reduction options and parameters.
    
    Parameters
    ----------
        check_reduction_wt : bool
            'check_reduction_wt' child.
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "reduce-picked-sample"

    argument_names = \
        ['check_reduction_wt', 'file_name', 'overwrite']

    check_reduction_wt: check_reduction_wt_cls = check_reduction_wt_cls
    """
    check_reduction_wt argument of reduce_picked_sample.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of reduce_picked_sample.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of reduce_picked_sample.
    """
