#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
class fast_solution(Command):
    """
    Write a FAST/Plot3D unstructured solution file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "fast-solution"

    argument_names = \
        ['name']

    name: name_cls = name_cls
    """
    name argument of fast_solution.
    """
