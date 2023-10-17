#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .surface_name_list import surface_name_list as surface_name_list_cls
from .structural_analysis import structural_analysis as structural_analysis_cls
from .write_loads import write_loads as write_loads_cls
from .loads import loads as loads_cls
class mechanical_apdl_input(Command):
    """
    Write an Mechanical APDL Input file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surface_name_list : typing.List[str]
            'surface_name_list' child.
        structural_analysis : bool
            'structural_analysis' child.
        write_loads : bool
            'write_loads' child.
        loads : typing.List[str]
            'loads' child.
    
    """

    fluent_name = "mechanical-apdl-input"

    argument_names = \
        ['name', 'surface_name_list', 'structural_analysis', 'write_loads',
         'loads']

    name: name_cls = name_cls
    """
    name argument of mechanical_apdl_input.
    """
    surface_name_list: surface_name_list_cls = surface_name_list_cls
    """
    surface_name_list argument of mechanical_apdl_input.
    """
    structural_analysis: structural_analysis_cls = structural_analysis_cls
    """
    structural_analysis argument of mechanical_apdl_input.
    """
    write_loads: write_loads_cls = write_loads_cls
    """
    write_loads argument of mechanical_apdl_input.
    """
    loads: loads_cls = loads_cls
    """
    loads argument of mechanical_apdl_input.
    """
