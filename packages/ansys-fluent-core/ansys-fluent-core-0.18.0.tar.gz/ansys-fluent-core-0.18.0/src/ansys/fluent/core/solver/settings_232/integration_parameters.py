#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .integration_method import integration_method as integration_method_cls
from .integration_options import integration_options as integration_options_cls
from .isat_options import isat_options as isat_options_cls
from .chemistry_agglomeration import chemistry_agglomeration as chemistry_agglomeration_cls
from .chemistry_agglomeration_options import chemistry_agglomeration_options as chemistry_agglomeration_options_cls
from .relax_to_equilibrium_options import relax_to_equilibrium_options as relax_to_equilibrium_options_cls
from .dynamic_mechanism_reduction import dynamic_mechanism_reduction as dynamic_mechanism_reduction_cls
from .dynamic_mechanism_reduction_options import dynamic_mechanism_reduction_options as dynamic_mechanism_reduction_options_cls
from .dimension_reduction import dimension_reduction as dimension_reduction_cls
from .dimension_reduction_mixture_options import dimension_reduction_mixture_options as dimension_reduction_mixture_options_cls
class integration_parameters(Group):
    """
    'integration_parameters' child.
    """

    fluent_name = "integration-parameters"

    child_names = \
        ['integration_method', 'integration_options', 'isat_options',
         'chemistry_agglomeration', 'chemistry_agglomeration_options',
         'relax_to_equilibrium_options', 'dynamic_mechanism_reduction',
         'dynamic_mechanism_reduction_options', 'dimension_reduction',
         'dimension_reduction_mixture_options']

    integration_method: integration_method_cls = integration_method_cls
    """
    integration_method child of integration_parameters.
    """
    integration_options: integration_options_cls = integration_options_cls
    """
    integration_options child of integration_parameters.
    """
    isat_options: isat_options_cls = isat_options_cls
    """
    isat_options child of integration_parameters.
    """
    chemistry_agglomeration: chemistry_agglomeration_cls = chemistry_agglomeration_cls
    """
    chemistry_agglomeration child of integration_parameters.
    """
    chemistry_agglomeration_options: chemistry_agglomeration_options_cls = chemistry_agglomeration_options_cls
    """
    chemistry_agglomeration_options child of integration_parameters.
    """
    relax_to_equilibrium_options: relax_to_equilibrium_options_cls = relax_to_equilibrium_options_cls
    """
    relax_to_equilibrium_options child of integration_parameters.
    """
    dynamic_mechanism_reduction: dynamic_mechanism_reduction_cls = dynamic_mechanism_reduction_cls
    """
    dynamic_mechanism_reduction child of integration_parameters.
    """
    dynamic_mechanism_reduction_options: dynamic_mechanism_reduction_options_cls = dynamic_mechanism_reduction_options_cls
    """
    dynamic_mechanism_reduction_options child of integration_parameters.
    """
    dimension_reduction: dimension_reduction_cls = dimension_reduction_cls
    """
    dimension_reduction child of integration_parameters.
    """
    dimension_reduction_mixture_options: dimension_reduction_mixture_options_cls = dimension_reduction_mixture_options_cls
    """
    dimension_reduction_mixture_options child of integration_parameters.
    """
