#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .report_type import report_type as report_type_cls
from .thread_id_list import thread_id_list as thread_id_list_cls
from .domain import domain as domain_cls
from .cell_function import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls
class volume_integrals(Command):
    """
    'volume_integrals' command.
    
    Parameters
    ----------
        report_type : str
            'report_type' child.
        thread_id_list : typing.List[str]
            'thread_id_list' child.
        domain : str
            'domain' child.
        cell_function : str
            'cell_function' child.
        current_domain : str
            'current_domain' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "volume-integrals"

    argument_names = \
        ['report_type', 'thread_id_list', 'domain', 'cell_function',
         'current_domain', 'write_to_file', 'file_name', 'append_data',
         'overwrite']

    report_type: report_type_cls = report_type_cls
    """
    report_type argument of volume_integrals.
    """
    thread_id_list: thread_id_list_cls = thread_id_list_cls
    """
    thread_id_list argument of volume_integrals.
    """
    domain: domain_cls = domain_cls
    """
    domain argument of volume_integrals.
    """
    cell_function: cell_function_cls = cell_function_cls
    """
    cell_function argument of volume_integrals.
    """
    current_domain: current_domain_cls = current_domain_cls
    """
    current_domain argument of volume_integrals.
    """
    write_to_file: write_to_file_cls = write_to_file_cls
    """
    write_to_file argument of volume_integrals.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of volume_integrals.
    """
    append_data: append_data_cls = append_data_cls
    """
    append_data argument of volume_integrals.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of volume_integrals.
    """
