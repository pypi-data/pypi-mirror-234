#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class run_calculation:
    fluent_name = ...
    child_names = ...
    adaptive_time_stepping = ...
    cfl_based_adaptive_time_stepping = ...
    data_sampling = ...
    transient_controls = ...
    command_names = ...

    def dual_time_iterate(self, number_of_total_periods: int, number_of_time_steps: int, total_number_of_time_steps: int, total_time: Union[float, str], incremental_time: Union[float, str], max_iteration_per_step: int, postprocess: bool, num_of_post_iter_per_timestep: int):
        """
        Perform unsteady iterations.
        
        Parameters
        ----------
            number_of_total_periods : int
                Set number of total periods.
            number_of_time_steps : int
                Set inceremtal number of Time steps.
            total_number_of_time_steps : int
                Set total number of Time steps.
            total_time : real
                Set Total Simulation Time.
            incremental_time : real
                Set Incremental Time.
            max_iteration_per_step : int
                Set Maximum Number of iterations per time step.
            postprocess : bool
                Enable/Disable Postprocess pollutant solution?.
            num_of_post_iter_per_timestep : int
                Set Number of post-processing iterations per time step.
        
        """

    def iterate(self, number_of_iterations: int):
        """
        Perform a specified number of iterations.
        
        Parameters
        ----------
            number_of_iterations : int
                Set inceremtal number of Time steps.
        
        """

