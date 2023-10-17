#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .remove_dataset import remove_dataset as remove_dataset_cls
from .list_datasets import list_datasets as list_datasets_cls
class data_sampling_options(Group):
    """
    Data sampling options for statistics.
    """

    fluent_name = "data-sampling-options"

    command_names = \
        ['remove_dataset', 'list_datasets']

    remove_dataset: remove_dataset_cls = remove_dataset_cls
    """
    remove_dataset command of data_sampling_options.
    """
    list_datasets: list_datasets_cls = list_datasets_cls
    """
    list_datasets command of data_sampling_options.
    """
