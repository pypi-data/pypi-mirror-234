#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .name import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .techplot_scalars import techplot_scalars as techplot_scalars_cls
class dx(Command):
    """
    Write an IBM Data Explorer format file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surfaces : typing.List[str]
            'surfaces' child.
        techplot_scalars : typing.List[str]
            'techplot_scalars' child.
    
    """

    fluent_name = "dx"

    argument_names = \
        ['name', 'surfaces', 'techplot_scalars']

    name: name_cls = name_cls
    """
    name argument of dx.
    """
    surfaces: surfaces_cls = surfaces_cls
    """
    surfaces argument of dx.
    """
    techplot_scalars: techplot_scalars_cls = techplot_scalars_cls
    """
    techplot_scalars argument of dx.
    """
