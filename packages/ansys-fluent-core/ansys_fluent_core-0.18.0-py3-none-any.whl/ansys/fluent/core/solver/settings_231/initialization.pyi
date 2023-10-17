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
    hybrid_init_options = ...
    patch = ...
    set_defaults = ...
    open_channel_auto_init = ...
    fmg_initialization = ...
    initialization_type = ...
    command_names = ...

    def standard_initialize(self, ):
        """
        Initialize the flow field with the current default values.
        """

    def hybrid_initialize(self, ):
        """
        Initialize using the hybrid initialization method.
        """

    def initialize(self, init_type: str):
        """
        'initialize' command.
        
        Parameters
        ----------
            init_type : str
                'init_type' child.
        
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

    def init_acoustics_options(self, set_ramping_length: bool, time_step_count: int):
        """
        'init_acoustics_options' command.
        
        Parameters
        ----------
            set_ramping_length : bool
                Enable/Disable ramping length and initialize acoustics.
            time_step_count : int
                Set number of timesteps for ramping of sources.
        
        """

    def list_defaults(self, ):
        """
        List default values.
        """

    def init_turb_vel_fluctuations(self, ):
        """
        Initialize turbulent velocity fluctuations.
        """

    def show_iterations_sampled(self, ):
        """
        'show_iterations_sampled' command.
        """

    def show_time_sampled(self, ):
        """
        Display the amount of simulated time covered by the data sampled for unsteady statistics.
        """

    def levelset_auto_init(self, ):
        """
        'levelset_auto_init' command.
        """

