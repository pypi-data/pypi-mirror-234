#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class partition:
    fluent_name = ...
    child_names = ...
    auto = ...
    set = ...
    command_names = ...

    def combine_partition(self, number_of_partitions: int):
        """
        Merge every N partitions.
        
        Parameters
        ----------
            number_of_partitions : int
                'number_of_partitions' child.
        
        """

    def merge_clusters(self, merge_iterations: int):
        """
        Merge partition clusters.
        
        Parameters
        ----------
            merge_iterations : int
                'merge_iterations' child.
        
        """

    def method(self, partition_method: str, count: int):
        """
        Partition the domain.
        
        Parameters
        ----------
            partition_method : str
                'partition_method' child.
            count : int
                'count' child.
        
        """

    def print_partitions(self, ):
        """
        Print partition information.
        """

    def print_active_partitions(self, ):
        """
        Print active partition information.
        """

    def print_stored_partitions(self, ):
        """
        Print stored partition information.
        """

    def reorder_partitions(self, ):
        """
        Reorder partitions.
        """

    def reorder_partitions_to_architecture(self, ):
        """
        Reorder partitions to architecture.
        """

    def smooth_partition(self, smoothing_iteration: int):
        """
        Smooth partition interface.
        
        Parameters
        ----------
            smoothing_iteration : int
                Set maximum number of smoothing iterations.
        
        """

    def use_stored_partitions(self, ):
        """
        Use stored partitioning.
        """

