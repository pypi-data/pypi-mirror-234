#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .ni import ni as ni_cls
from .nj import nj as nj_cls
from .nk import nk as nk_cls
from .xe import xe as xe_cls
from .len import len as len_cls
class beach_dir_list_child(Group):
    """
    'child_object_type' of beach_dir_list.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['ni', 'nj', 'nk', 'xe', 'len']

    ni: ni_cls = ni_cls
    """
    ni child of beach_dir_list_child.
    """
    nj: nj_cls = nj_cls
    """
    nj child of beach_dir_list_child.
    """
    nk: nk_cls = nk_cls
    """
    nk child of beach_dir_list_child.
    """
    xe: xe_cls = xe_cls
    """
    xe child of beach_dir_list_child.
    """
    len: len_cls = len_cls
    """
    len child of beach_dir_list_child.
    """
