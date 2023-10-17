#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .read import read as read_cls
from .replace_mesh import replace_mesh as replace_mesh_cls
from .write import write as write_cls
from .parametric_project import parametric_project as parametric_project_cls
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    command_names = \
        ['read', 'replace_mesh', 'write', 'parametric_project']

    read: read_cls = read_cls
    """
    read command of file.
    """
    replace_mesh: replace_mesh_cls = replace_mesh_cls
    """
    replace_mesh command of file.
    """
    write: write_cls = write_cls
    """
    write command of file.
    """
    parametric_project: parametric_project_cls = parametric_project_cls
    """
    parametric_project command of file.
    """
