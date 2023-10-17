#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .user_specified_species import user_specified_species as user_specified_species_cls
from .species_1 import species as species_cls
class species_setting(Group):
    """
    Enter the species settings menu.
    """

    fluent_name = "species-setting"

    child_names = \
        ['user_specified_species', 'species']

    user_specified_species: user_specified_species_cls = user_specified_species_cls
    """
    user_specified_species child of species_setting.
    """
    species: species_cls = species_cls
    """
    species child of species_setting.
    """
