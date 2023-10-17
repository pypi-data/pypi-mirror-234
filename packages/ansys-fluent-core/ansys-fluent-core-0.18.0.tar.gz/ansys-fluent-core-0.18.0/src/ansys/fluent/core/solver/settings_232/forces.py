#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .options import options as options_cls
from .domain_val import domain_val as domain_val_cls
from .all_wall_zones import all_wall_zones as all_wall_zones_cls
from .wall_thread_list import wall_thread_list as wall_thread_list_cls
from .direction_vector_1 import direction_vector as direction_vector_cls
from .momentum_center import momentum_center as momentum_center_cls
from .momentum_axis import momentum_axis as momentum_axis_cls
from .pressure_coordinate import pressure_coordinate as pressure_coordinate_cls
from .coord_val import coord_val as coord_val_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls
class forces(Command):
    """
    'forces' command.
    
    Parameters
    ----------
        options : str
            'options' child.
        domain_val : str
            'domain_val' child.
        all_wall_zones : bool
            Select all wall zones available.
        wall_thread_list : typing.List[str]
            'wall_thread_list' child.
        direction_vector : typing.List[real]
            'direction_vector' child.
        momentum_center : typing.List[real]
            'momentum_center' child.
        momentum_axis : typing.List[real]
            'momentum_axis' child.
        pressure_coordinate : str
            'pressure_coordinate' child.
        coord_val : real
            'coord_val' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "forces"

    argument_names = \
        ['options', 'domain_val', 'all_wall_zones', 'wall_thread_list',
         'direction_vector', 'momentum_center', 'momentum_axis',
         'pressure_coordinate', 'coord_val', 'write_to_file', 'file_name',
         'append_data', 'overwrite']

    options: options_cls = options_cls
    """
    options argument of forces.
    """
    domain_val: domain_val_cls = domain_val_cls
    """
    domain_val argument of forces.
    """
    all_wall_zones: all_wall_zones_cls = all_wall_zones_cls
    """
    all_wall_zones argument of forces.
    """
    wall_thread_list: wall_thread_list_cls = wall_thread_list_cls
    """
    wall_thread_list argument of forces.
    """
    direction_vector: direction_vector_cls = direction_vector_cls
    """
    direction_vector argument of forces.
    """
    momentum_center: momentum_center_cls = momentum_center_cls
    """
    momentum_center argument of forces.
    """
    momentum_axis: momentum_axis_cls = momentum_axis_cls
    """
    momentum_axis argument of forces.
    """
    pressure_coordinate: pressure_coordinate_cls = pressure_coordinate_cls
    """
    pressure_coordinate argument of forces.
    """
    coord_val: coord_val_cls = coord_val_cls
    """
    coord_val argument of forces.
    """
    write_to_file: write_to_file_cls = write_to_file_cls
    """
    write_to_file argument of forces.
    """
    file_name: file_name_cls = file_name_cls
    """
    file_name argument of forces.
    """
    append_data: append_data_cls = append_data_cls
    """
    append_data argument of forces.
    """
    overwrite: overwrite_cls = overwrite_cls
    """
    overwrite argument of forces.
    """
