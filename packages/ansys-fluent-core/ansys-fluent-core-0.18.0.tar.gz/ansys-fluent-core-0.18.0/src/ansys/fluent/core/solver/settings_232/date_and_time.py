#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .day import day as day_cls
from .month import month as month_cls
from .hour import hour as hour_cls
from .minute import minute as minute_cls
class date_and_time(Group):
    """
    'date_and_time' child.
    """

    fluent_name = "date-and-time"

    child_names = \
        ['day', 'month', 'hour', 'minute']

    day: day_cls = day_cls
    """
    day child of date_and_time.
    """
    month: month_cls = month_cls
    """
    month child of date_and_time.
    """
    hour: hour_cls = hour_cls
    """
    hour child of date_and_time.
    """
    minute: minute_cls = minute_cls
    """
    minute child of date_and_time.
    """
