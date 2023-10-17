#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .number_of_represented_species import number_of_represented_species as number_of_represented_species_cls
from .full_mechanism_material_name import full_mechanism_material_name as full_mechanism_material_name_cls
from .fuel_oxidizer_species import fuel_oxidizer_species as fuel_oxidizer_species_cls
class dimension_reduction_mixture_options(Group):
    """
    'dimension_reduction_mixture_options' child.
    """

    fluent_name = "dimension-reduction-mixture-options"

    child_names = \
        ['number_of_represented_species', 'full_mechanism_material_name',
         'fuel_oxidizer_species']

    number_of_represented_species: number_of_represented_species_cls = number_of_represented_species_cls
    """
    number_of_represented_species child of dimension_reduction_mixture_options.
    """
    full_mechanism_material_name: full_mechanism_material_name_cls = full_mechanism_material_name_cls
    """
    full_mechanism_material_name child of dimension_reduction_mixture_options.
    """
    fuel_oxidizer_species: fuel_oxidizer_species_cls = fuel_oxidizer_species_cls
    """
    fuel_oxidizer_species child of dimension_reduction_mixture_options.
    """
