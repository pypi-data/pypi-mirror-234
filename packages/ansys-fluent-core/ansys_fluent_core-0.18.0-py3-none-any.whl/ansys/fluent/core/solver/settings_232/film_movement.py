#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .condensing_film import condensing_film as condensing_film_cls
from .all_film import all_film as all_film_cls
class film_movement(Group):
    """
    Set options for controlling the film particles movement.
    """

    fluent_name = "film-movement"

    child_names = \
        ['condensing_film', 'all_film']

    condensing_film: condensing_film_cls = condensing_film_cls
    """
    condensing_film child of film_movement.
    """
    all_film: all_film_cls = all_film_cls
    """
    all_film child of film_movement.
    """
