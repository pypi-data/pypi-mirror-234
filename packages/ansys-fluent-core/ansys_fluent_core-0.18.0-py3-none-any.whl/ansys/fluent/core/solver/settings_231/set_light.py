#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .light_number import light_number as light_number_cls
from .light_on import light_on as light_on_cls
from .rgb_vector import rgb_vector as rgb_vector_cls
from .use_view_factor import use_view_factor as use_view_factor_cls
from .change_light_direction import change_light_direction as change_light_direction_cls
from .direction_vector_1 import direction_vector as direction_vector_cls
class set_light(Command):
    """
    'set_light' command.
    
    Parameters
    ----------
        light_number : int
            'light_number' child.
        light_on : bool
            'light_on' child.
        rgb_vector : typing.Tuple[real, real, real]
            'rgb_vector' child.
        use_view_factor : bool
            'use_view_factor' child.
        change_light_direction : bool
            'change_light_direction' child.
        direction_vector : typing.Tuple[real, real, real]
            'direction_vector' child.
    
    """

    fluent_name = "set-light"

    argument_names = \
        ['light_number', 'light_on', 'rgb_vector', 'use_view_factor',
         'change_light_direction', 'direction_vector']

    light_number: light_number_cls = light_number_cls
    """
    light_number argument of set_light.
    """
    light_on: light_on_cls = light_on_cls
    """
    light_on argument of set_light.
    """
    rgb_vector: rgb_vector_cls = rgb_vector_cls
    """
    rgb_vector argument of set_light.
    """
    use_view_factor: use_view_factor_cls = use_view_factor_cls
    """
    use_view_factor argument of set_light.
    """
    change_light_direction: change_light_direction_cls = change_light_direction_cls
    """
    change_light_direction argument of set_light.
    """
    direction_vector: direction_vector_cls = direction_vector_cls
    """
    direction_vector argument of set_light.
    """
