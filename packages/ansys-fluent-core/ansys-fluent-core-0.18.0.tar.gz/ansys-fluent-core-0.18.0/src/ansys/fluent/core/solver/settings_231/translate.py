#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .offset import offset as offset_cls
class translate(Command):
    """
    Translate the mesh.
    
    Parameters
    ----------
        offset : typing.Tuple[real, real, real]
            'offset' child.
    
    """

    fluent_name = "translate"

    argument_names = \
        ['offset']

    offset: offset_cls = offset_cls
    """
    offset argument of translate.
    """
