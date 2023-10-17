#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class initialization:
    fluent_name = ...
    child_names = ...
    initialization_type = ...
    reference_frame = ...
    defaults = ...
    fmg_options = ...
    localized_turb_init = ...
    hybrid_init_options = ...
    patch = ...
    open_channel_auto_init = ...
    fmg_initialization = ...
    command_names = ...

    def initialize(self, ):
        """
        'initialize' command.
        """

    def compute_defaults(self, from_zone_type: str, from_zone_name: str, phase: str):
        """
        'compute_defaults' command.
        
        Parameters
        ----------
            from_zone_type : str
                'from_zone_type' child.
            from_zone_name : str
                'from_zone_name' child.
            phase : str
                'phase' child.
        
        """

    def fmg_initialize(self, ):
        """
        Initialize using the full-multigrid initialization (FMG).
        """

    def standard_initialize(self, ):
        """
        Initialize the flow field with the current default values.
        """

    def hybrid_initialize(self, ):
        """
        Initialize using the hybrid initialization method.
        """

    def list_defaults(self, ):
        """
        List default values.
        """

    def init_turb_vel_fluctuations(self, ):
        """
        Initialize turbulent velocity fluctuations.
        """

    def init_flow_statistics(self, ):
        """
        Initialize statistics.
        """

    def show_iterations_sampled(self, ):
        """
        'show_iterations_sampled' command.
        """

    def show_time_sampled(self, ):
        """
        Display the amount of simulated time covered by the data sampled for unsteady statistics.
        """

    def dpm_reset(self, ):
        """
        Reset discrete phase source terms to zero.
        """

    def lwf_reset(self, ):
        """
        Delete wall film particles and initialize wall film variables to zero.
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

    def levelset_auto_init(self, ):
        """
        'levelset_auto_init' command.
        """

