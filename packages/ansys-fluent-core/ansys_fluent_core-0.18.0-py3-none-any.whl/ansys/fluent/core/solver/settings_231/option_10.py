#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .min_max import min_max as min_max_cls
from .in_range import in_range as in_range_cls
from .except_in_range import except_in_range as except_in_range_cls
from .top_value_cells import top_value_cells as top_value_cells_cls
from .low_value_cells import low_value_cells as low_value_cells_cls
from .less_than import less_than as less_than_cls
from .more_than import more_than as more_than_cls
from .between_std_dev import between_std_dev as between_std_dev_cls
from .outside_std_dev import outside_std_dev as outside_std_dev_cls
from .less_than_std_dev import less_than_std_dev as less_than_std_dev_cls
from .more_than_std_dev import more_than_std_dev as more_than_std_dev_cls
class option(Group):
    """
    'option' child.
    """

    fluent_name = "option"

    child_names = \
        ['option', 'min_max', 'in_range', 'except_in_range',
         'top_value_cells', 'low_value_cells', 'less_than', 'more_than',
         'between_std_dev', 'outside_std_dev', 'less_than_std_dev',
         'more_than_std_dev']

    option: option_cls = option_cls
    """
    option child of option.
    """
    min_max: min_max_cls = min_max_cls
    """
    min_max child of option.
    """
    in_range: in_range_cls = in_range_cls
    """
    in_range child of option.
    """
    except_in_range: except_in_range_cls = except_in_range_cls
    """
    except_in_range child of option.
    """
    top_value_cells: top_value_cells_cls = top_value_cells_cls
    """
    top_value_cells child of option.
    """
    low_value_cells: low_value_cells_cls = low_value_cells_cls
    """
    low_value_cells child of option.
    """
    less_than: less_than_cls = less_than_cls
    """
    less_than child of option.
    """
    more_than: more_than_cls = more_than_cls
    """
    more_than child of option.
    """
    between_std_dev: between_std_dev_cls = between_std_dev_cls
    """
    between_std_dev child of option.
    """
    outside_std_dev: outside_std_dev_cls = outside_std_dev_cls
    """
    outside_std_dev child of option.
    """
    less_than_std_dev: less_than_std_dev_cls = less_than_std_dev_cls
    """
    less_than_std_dev child of option.
    """
    more_than_std_dev: more_than_std_dev_cls = more_than_std_dev_cls
    """
    more_than_std_dev child of option.
    """
