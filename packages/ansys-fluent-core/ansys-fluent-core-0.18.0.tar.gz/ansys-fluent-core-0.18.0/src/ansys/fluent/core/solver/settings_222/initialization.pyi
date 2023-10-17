#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class initialization:
    fluent_name = ...
    child_names = ...
    fmg_initialize = ...
    localized_turb_init = ...
    reference_frame = ...
    fmg_options = ...
    set_hybrid_init_options = ...
    patch = ...
    command_names = ...

    def standard_initialize(self, ):
        """
        Initialize the flow field with the current default values.
        """

    def hybrid_initialize(self, ):
        """
        Initialize using the hybrid initialization method.
        """

    def dpm_reset(self, ):
        """
        Reset discrete phase source terms to zero.
        """

    def lwf_reset(self, ):
        """
        Delete wall film particles and initialize wall film variables to zero.
        """

    def init_flow_statistics(self, ):
        """
        Initialize statistics.
        """

    def init_acoustics_options(self, set_ramping_length: bool, number_of_timesteps: int):
        """
        'init_acoustics_options' command.
        
        Parameters
        ----------
            set_ramping_length : bool
                Enable/Disable ramping length and initialize acoustics.
            number_of_timesteps : int
                Set number of timesteps for ramping of sources.
        
        """

