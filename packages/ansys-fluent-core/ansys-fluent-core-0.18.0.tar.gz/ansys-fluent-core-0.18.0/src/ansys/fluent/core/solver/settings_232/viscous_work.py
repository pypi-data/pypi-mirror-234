#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .domain_val import domain_val as domain_val_cls
from .all_bndry_zones import all_bndry_zones as all_bndry_zones_cls
from .zone_list import zone_list as zone_list_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls
class viscous_work(Command):
    """
    Print viscous work rate at boundaries.
    
    Parameters
    ----------
        domain_val : str
            'domain_val' child.
        all_bndry_zones : bool
            Select all the boundary/interior zones.
        zone_list : typing.List[str]
            'zone_list' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "viscous-work"

    argument_names = \
        ['domain_val', 'all_bndry_zones', 'zone_list', 'write_to_file',
         'file_name', 'append_data', 'overwrite']

    domain_val: domain_val_cls = domain_val_cls
    """
    domain_val argument of viscous_work.
    """
    all_bndry_zones: all_bndry_zones_cls = all_bndry_zones_cls
    """
    all_bndry_zones argument of viscous_work.
    """
    zone_list: zone_list_cls = zone_list_cls
    """
    zone_list argument of viscous_work.
    """
    write_to_file: write_to_file_cls = write_to_file_cls
    """
    write_to_file argument of viscous_work.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of viscous_work.
    """
    append_data: append_data_cls = append_data_cls
    """
    append_data argument of viscous_work.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of viscous_work.
    """
