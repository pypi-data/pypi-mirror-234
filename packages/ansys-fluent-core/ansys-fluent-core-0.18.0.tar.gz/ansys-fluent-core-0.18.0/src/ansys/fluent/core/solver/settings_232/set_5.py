#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .coupling import coupling as coupling_cls
from .helper_session_setup import helper_session_setup as helper_session_setup_cls
from .helper_session import helper_session as helper_session_cls
class set(Group):
    """
    'set' child.
    """

    fluent_name = "set"

    child_names = \
        ['coupling', 'helper_session_setup', 'helper_session']

    coupling: coupling_cls = coupling_cls
    """
    coupling child of set.
    """
    helper_session_setup: helper_session_setup_cls = helper_session_setup_cls
    """
    helper_session_setup child of set.
    """
    helper_session: helper_session_cls = helper_session_cls
    """
    helper_session child of set.
    """
