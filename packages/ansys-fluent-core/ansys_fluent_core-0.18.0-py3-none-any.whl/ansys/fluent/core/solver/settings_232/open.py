#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .project_filename import project_filename as project_filename_cls
from .load_case import load_case as load_case_cls
class open(Command):
    """
    Open project.
    
    Parameters
    ----------
        project_filename : str
            'project_filename' child.
        load_case : bool
            'load_case' child.
    
    """

    fluent_name = "open"

    argument_names = \
        ['project_filename', 'load_case']

    project_filename: project_filename_cls = project_filename_cls
    """
    project_filename argument of open.
    """
    load_case: load_case_cls = load_case_cls
    """
    load_case argument of open.
    """
