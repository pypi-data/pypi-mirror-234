#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .particle_species import particle_species as particle_species_cls
from .last_species import last_species as last_species_cls
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['particle_species', 'last_species']

    particle_species: particle_species_cls = particle_species_cls
    """
    particle_species child of species.
    """
    last_species: last_species_cls = last_species_cls
    """
    last_species child of species.
    """
