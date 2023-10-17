#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .case_frequency import case_frequency as case_frequency_cls
from .data_frequency import data_frequency as data_frequency_cls
from .root_name import root_name as root_name_cls
from .retain_most_recent_files import retain_most_recent_files as retain_most_recent_files_cls
from .max_files import max_files as max_files_cls
from .append_file_name_with import append_file_name_with as append_file_name_with_cls
from .save_data_file_every import save_data_file_every as save_data_file_every_cls
class auto_save(Group):
    """
    'auto_save' child.
    """

    fluent_name = "auto-save"

    child_names = \
        ['case_frequency', 'data_frequency', 'root_name',
         'retain_most_recent_files', 'max_files', 'append_file_name_with',
         'save_data_file_every']

    case_frequency: case_frequency_cls = case_frequency_cls
    """
    case_frequency child of auto_save.
    """
    data_frequency: data_frequency_cls = data_frequency_cls
    """
    data_frequency child of auto_save.
    """
    root_name: root_name_cls = root_name_cls
    """
    root_name child of auto_save.
    """
    retain_most_recent_files: retain_most_recent_files_cls = retain_most_recent_files_cls
    """
    retain_most_recent_files child of auto_save.
    """
    max_files: max_files_cls = max_files_cls
    """
    max_files child of auto_save.
    """
    append_file_name_with: append_file_name_with_cls = append_file_name_with_cls
    """
    append_file_name_with child of auto_save.
    """
    save_data_file_every: save_data_file_every_cls = save_data_file_every_cls
    """
    save_data_file_every child of auto_save.
    """
