#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .single_precision_coordinates import single_precision_coordinates as single_precision_coordinates_cls
from .binary_legacy_files import binary_legacy_files as binary_legacy_files_cls
from .cff_files import cff_files as cff_files_cls
from .async_optimize import async_optimize as async_optimize_cls
from .write_pdat import write_pdat as write_pdat_cls
from .confirm_overwrite import confirm_overwrite as confirm_overwrite_cls
from .export import export as export_cls
from .import_ import import_ as import__cls
from .parametric_project import parametric_project as parametric_project_cls
from .auto_save import auto_save as auto_save_cls
from .define_macro import define_macro as define_macro_cls
from .read_1 import read as read_cls
from .read_case import read_case as read_case_cls
from .read_case_data import read_case_data as read_case_data_cls
from .read_case_setting import read_case_setting as read_case_setting_cls
from .read_data import read_data as read_data_cls
from .read_mesh import read_mesh as read_mesh_cls
from .read_journal import read_journal as read_journal_cls
from .start_journal import start_journal as start_journal_cls
from .stop_journal import stop_journal as stop_journal_cls
from .replace_mesh import replace_mesh as replace_mesh_cls
from .write import write as write_cls
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    child_names = \
        ['single_precision_coordinates', 'binary_legacy_files', 'cff_files',
         'async_optimize', 'write_pdat', 'confirm_overwrite', 'export',
         'import_', 'parametric_project']

    single_precision_coordinates: single_precision_coordinates_cls = single_precision_coordinates_cls
    """
    single_precision_coordinates child of file.
    """
    binary_legacy_files: binary_legacy_files_cls = binary_legacy_files_cls
    """
    binary_legacy_files child of file.
    """
    cff_files: cff_files_cls = cff_files_cls
    """
    cff_files child of file.
    """
    async_optimize: async_optimize_cls = async_optimize_cls
    """
    async_optimize child of file.
    """
    write_pdat: write_pdat_cls = write_pdat_cls
    """
    write_pdat child of file.
    """
    confirm_overwrite: confirm_overwrite_cls = confirm_overwrite_cls
    """
    confirm_overwrite child of file.
    """
    export: export_cls = export_cls
    """
    export child of file.
    """
    import_: import__cls = import__cls
    """
    import_ child of file.
    """
    parametric_project: parametric_project_cls = parametric_project_cls
    """
    parametric_project child of file.
    """
    command_names = \
        ['auto_save', 'define_macro', 'read', 'read_case', 'read_case_data',
         'read_case_setting', 'read_data', 'read_mesh', 'read_journal',
         'start_journal', 'stop_journal', 'replace_mesh', 'write']

    auto_save: auto_save_cls = auto_save_cls
    """
    auto_save command of file.
    """
    define_macro: define_macro_cls = define_macro_cls
    """
    define_macro command of file.
    """
    read: read_cls = read_cls
    """
    read command of file.
    """
    read_case: read_case_cls = read_case_cls
    """
    read_case command of file.
    """
    read_case_data: read_case_data_cls = read_case_data_cls
    """
    read_case_data command of file.
    """
    read_case_setting: read_case_setting_cls = read_case_setting_cls
    """
    read_case_setting command of file.
    """
    read_data: read_data_cls = read_data_cls
    """
    read_data command of file.
    """
    read_mesh: read_mesh_cls = read_mesh_cls
    """
    read_mesh command of file.
    """
    read_journal: read_journal_cls = read_journal_cls
    """
    read_journal command of file.
    """
    start_journal: start_journal_cls = start_journal_cls
    """
    start_journal command of file.
    """
    stop_journal: stop_journal_cls = stop_journal_cls
    """
    stop_journal command of file.
    """
    replace_mesh: replace_mesh_cls = replace_mesh_cls
    """
    replace_mesh command of file.
    """
    write: write_cls = write_cls
    """
    write command of file.
    """
