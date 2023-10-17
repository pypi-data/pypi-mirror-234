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
from .convert_hanging_nodes_during_read import convert_hanging_nodes_during_read as convert_hanging_nodes_during_read_cls
from .async_optimize import async_optimize as async_optimize_cls
from .write_pdat import write_pdat as write_pdat_cls
from .confirm_overwrite import confirm_overwrite as confirm_overwrite_cls
from .auto_save import auto_save as auto_save_cls
from .export import export as export_cls
from .import_ import import_ as import__cls
from .parametric_project import parametric_project as parametric_project_cls
from .cffio_options import cffio_options as cffio_options_cls
from .define_macro import define_macro as define_macro_cls
from .execute_macro import execute_macro as execute_macro_cls
from .read_macros import read_macros as read_macros_cls
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
from .read_settings import read_settings as read_settings_cls
from .read_field_functions import read_field_functions as read_field_functions_cls
from .read_injections import read_injections as read_injections_cls
from .read_profile import read_profile as read_profile_cls
from .read_pdf import read_pdf as read_pdf_cls
from .read_isat_table import read_isat_table as read_isat_table_cls
from .show_configuration import show_configuration as show_configuration_cls
from .stop_macro import stop_macro as stop_macro_cls
from .start_transcript import start_transcript as start_transcript_cls
from .stop_transcript import stop_transcript as stop_transcript_cls
from .data_file_options import data_file_options as data_file_options_cls
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    child_names = \
        ['single_precision_coordinates', 'binary_legacy_files', 'cff_files',
         'convert_hanging_nodes_during_read', 'async_optimize', 'write_pdat',
         'confirm_overwrite', 'auto_save', 'export', 'import_',
         'parametric_project', 'cffio_options']

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
    convert_hanging_nodes_during_read: convert_hanging_nodes_during_read_cls = convert_hanging_nodes_during_read_cls
    """
    convert_hanging_nodes_during_read child of file.
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
    auto_save: auto_save_cls = auto_save_cls
    """
    auto_save child of file.
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
    cffio_options: cffio_options_cls = cffio_options_cls
    """
    cffio_options child of file.
    """
    command_names = \
        ['define_macro', 'execute_macro', 'read_macros', 'read', 'read_case',
         'read_case_data', 'read_case_setting', 'read_data', 'read_mesh',
         'read_journal', 'start_journal', 'stop_journal', 'replace_mesh',
         'write', 'read_settings', 'read_field_functions', 'read_injections',
         'read_profile', 'read_pdf', 'read_isat_table', 'show_configuration',
         'stop_macro', 'start_transcript', 'stop_transcript',
         'data_file_options']

    define_macro: define_macro_cls = define_macro_cls
    """
    define_macro command of file.
    """
    execute_macro: execute_macro_cls = execute_macro_cls
    """
    execute_macro command of file.
    """
    read_macros: read_macros_cls = read_macros_cls
    """
    read_macros command of file.
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
    read_settings: read_settings_cls = read_settings_cls
    """
    read_settings command of file.
    """
    read_field_functions: read_field_functions_cls = read_field_functions_cls
    """
    read_field_functions command of file.
    """
    read_injections: read_injections_cls = read_injections_cls
    """
    read_injections command of file.
    """
    read_profile: read_profile_cls = read_profile_cls
    """
    read_profile command of file.
    """
    read_pdf: read_pdf_cls = read_pdf_cls
    """
    read_pdf command of file.
    """
    read_isat_table: read_isat_table_cls = read_isat_table_cls
    """
    read_isat_table command of file.
    """
    show_configuration: show_configuration_cls = show_configuration_cls
    """
    show_configuration command of file.
    """
    stop_macro: stop_macro_cls = stop_macro_cls
    """
    stop_macro command of file.
    """
    start_transcript: start_transcript_cls = start_transcript_cls
    """
    start_transcript command of file.
    """
    stop_transcript: stop_transcript_cls = stop_transcript_cls
    """
    stop_transcript command of file.
    """
    data_file_options: data_file_options_cls = data_file_options_cls
    """
    data_file_options command of file.
    """
