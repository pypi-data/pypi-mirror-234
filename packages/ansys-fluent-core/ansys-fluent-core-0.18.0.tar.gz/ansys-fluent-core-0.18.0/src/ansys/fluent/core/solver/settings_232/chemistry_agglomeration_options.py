#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .chemistry_agglomeration_error_tolerance import chemistry_agglomeration_error_tolerance as chemistry_agglomeration_error_tolerance_cls
from .chemistry_agglomeration_temperature_bin import chemistry_agglomeration_temperature_bin as chemistry_agglomeration_temperature_bin_cls
class chemistry_agglomeration_options(Group):
    """
    'chemistry_agglomeration_options' child.
    """

    fluent_name = "chemistry-agglomeration-options"

    child_names = \
        ['chemistry_agglomeration_error_tolerance',
         'chemistry_agglomeration_temperature_bin']

    chemistry_agglomeration_error_tolerance: chemistry_agglomeration_error_tolerance_cls = chemistry_agglomeration_error_tolerance_cls
    """
    chemistry_agglomeration_error_tolerance child of chemistry_agglomeration_options.
    """
    chemistry_agglomeration_temperature_bin: chemistry_agglomeration_temperature_bin_cls = chemistry_agglomeration_temperature_bin_cls
    """
    chemistry_agglomeration_temperature_bin child of chemistry_agglomeration_options.
    """
