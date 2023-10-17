#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .edc_pasr_mixing_model import edc_pasr_mixing_model as edc_pasr_mixing_model_cls
from .mixing_constant import mixing_constant as mixing_constant_cls
from .fractal_dimension import fractal_dimension as fractal_dimension_cls
class edc_pasr_model_options(Group):
    """
    'edc_pasr_model_options' child.
    """

    fluent_name = "edc-pasr-model-options"

    child_names = \
        ['edc_pasr_mixing_model', 'mixing_constant', 'fractal_dimension']

    edc_pasr_mixing_model: edc_pasr_mixing_model_cls = edc_pasr_mixing_model_cls
    """
    edc_pasr_mixing_model child of edc_pasr_model_options.
    """
    mixing_constant: mixing_constant_cls = mixing_constant_cls
    """
    mixing_constant child of edc_pasr_model_options.
    """
    fractal_dimension: fractal_dimension_cls = fractal_dimension_cls
    """
    fractal_dimension child of edc_pasr_model_options.
    """
