#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .option_2 import option as option_cls
from .cone_type import cone_type as cone_type_cls
from .inject_as_film import inject_as_film as inject_as_film_cls
class injection_type(Group):
    """
    'injection_type' child.
    """

    fluent_name = "injection-type"

    child_names = \
        ['option', 'cone_type', 'inject_as_film']

    option: option_cls = option_cls
    """
    option child of injection_type.
    """
    cone_type: cone_type_cls = cone_type_cls
    """
    cone_type child of injection_type.
    """
    inject_as_film: inject_as_film_cls = inject_as_film_cls
    """
    inject_as_film child of injection_type.
    """
