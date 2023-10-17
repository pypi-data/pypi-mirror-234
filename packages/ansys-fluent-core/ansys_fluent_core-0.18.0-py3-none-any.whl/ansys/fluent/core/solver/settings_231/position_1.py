#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .xyz import xyz as xyz_cls
class position(Command):
    """
    Set the camera position.
    
    Parameters
    ----------
        xyz : typing.List[real]
            'xyz' child.
    
    """

    fluent_name = "position"

    argument_names = \
        ['xyz']

    xyz: xyz_cls = xyz_cls
    """
    xyz argument of position.
    """
