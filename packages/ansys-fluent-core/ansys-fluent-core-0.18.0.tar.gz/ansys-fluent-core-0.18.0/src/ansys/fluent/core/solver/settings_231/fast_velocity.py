#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
class fast_velocity(Command):
    """
    Write a FAST/Plot3D unstructured vector function file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "fast-velocity"

    argument_names = \
        ['name']

    name: name_cls = name_cls
    """
    name argument of fast_velocity.
    """
