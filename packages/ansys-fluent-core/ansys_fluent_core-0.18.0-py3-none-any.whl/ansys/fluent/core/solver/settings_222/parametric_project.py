#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .new import new as new_cls
from .open import open as open_cls
from .save import save as save_cls
from .save_as import save_as as save_as_cls
from .save_as_copy import save_as_copy as save_as_copy_cls
from .archive import archive as archive_cls
class parametric_project(Group):
    """
    'parametric_project' child.
    """

    fluent_name = "parametric-project"

    command_names = \
        ['new', 'open', 'save', 'save_as', 'save_as_copy', 'archive']

    new: new_cls = new_cls
    """
    new command of parametric_project.
    """
    open: open_cls = open_cls
    """
    open command of parametric_project.
    """
    save: save_cls = save_cls
    """
    save command of parametric_project.
    """
    save_as: save_as_cls = save_as_cls
    """
    save_as command of parametric_project.
    """
    save_as_copy: save_as_copy_cls = save_as_copy_cls
    """
    save_as_copy command of parametric_project.
    """
    archive: archive_cls = archive_cls
    """
    archive command of parametric_project.
    """
