#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .zones_1 import zones as zones_cls
class display(Command):
    """
    Display specified mesh interface zone.
    
    Parameters
    ----------
        zones : typing.List[int]
            'zones' child.
    
    """

    fluent_name = "display"

    argument_names = \
        ['zones']

    zones: zones_cls = zones_cls
    """
    zones argument of display.
    """
