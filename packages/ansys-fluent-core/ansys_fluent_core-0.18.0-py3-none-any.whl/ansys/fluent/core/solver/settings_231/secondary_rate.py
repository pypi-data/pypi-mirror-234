#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .particle_thermolysis_rate import particle_thermolysis_rate as particle_thermolysis_rate_cls
from .film_thermolysis_rate import film_thermolysis_rate as film_thermolysis_rate_cls
class secondary_rate(Group):
    """
    'secondary_rate' child.
    """

    fluent_name = "secondary-rate"

    child_names = \
        ['particle_thermolysis_rate', 'film_thermolysis_rate']

    particle_thermolysis_rate: particle_thermolysis_rate_cls = particle_thermolysis_rate_cls
    """
    particle_thermolysis_rate child of secondary_rate.
    """
    film_thermolysis_rate: film_thermolysis_rate_cls = film_thermolysis_rate_cls
    """
    film_thermolysis_rate child of secondary_rate.
    """
