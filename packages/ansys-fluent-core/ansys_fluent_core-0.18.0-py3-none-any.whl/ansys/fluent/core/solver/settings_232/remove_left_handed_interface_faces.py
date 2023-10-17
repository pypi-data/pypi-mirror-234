#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .enable_8 import enable as enable_cls
from .update_1 import update as update_cls
class remove_left_handed_interface_faces(Command):
    """
    Remove left-handed faces during mesh interface creation.
    
    Parameters
    ----------
        enable : bool
            Remove left-handed faces on mesh interfaces.
        update : bool
            'update' child.
    
    """

    fluent_name = "remove-left-handed-interface-faces?"

    argument_names = \
        ['enable', 'update']

    enable: enable_cls = enable_cls
    """
    enable argument of remove_left_handed_interface_faces.
    """
    update: update_cls = update_cls
    """
    update argument of remove_left_handed_interface_faces.
    """
