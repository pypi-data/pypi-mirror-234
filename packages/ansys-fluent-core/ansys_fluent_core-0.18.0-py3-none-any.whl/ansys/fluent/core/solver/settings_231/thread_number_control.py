#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .thread_number_method import thread_number_method as thread_number_method_cls
from .fixed_thread_number import fixed_thread_number as fixed_thread_number_cls
class thread_number_control(Group):
    """
    Thread number control.
    """

    fluent_name = "thread-number-control"

    child_names = \
        ['thread_number_method', 'fixed_thread_number']

    thread_number_method: thread_number_method_cls = thread_number_method_cls
    """
    thread_number_method child of thread_number_control.
    """
    fixed_thread_number: fixed_thread_number_cls = fixed_thread_number_cls
    """
    fixed_thread_number child of thread_number_control.
    """
