#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .copy import copy as copy_cls
from .list_beam_parameters import list_beam_parameters as list_beam_parameters_cls
from .beams_child import beams_child

class beams(NamedObject[beams_child], _CreatableNamedObjectMixin[beams_child]):
    """
    Enter the optical beams menu.
    """

    fluent_name = "beams"

    command_names = \
        ['copy', 'list_beam_parameters']

    copy: copy_cls = copy_cls
    """
    copy command of beams.
    """
    list_beam_parameters: list_beam_parameters_cls = list_beam_parameters_cls
    """
    list_beam_parameters command of beams.
    """
    child_object_type: beams_child = beams_child
    """
    child_object_type of beams.
    """
