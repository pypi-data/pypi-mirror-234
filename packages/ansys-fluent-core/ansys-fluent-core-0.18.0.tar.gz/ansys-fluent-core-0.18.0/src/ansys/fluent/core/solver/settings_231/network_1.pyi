#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class network:
    fluent_name = ...
    child_names = ...
    shell_script_path = ...
    command_names = ...

    def kill_all_nodes(self, invalidate_case: bool, delete_all_compute_nodes: bool):
        """
        Delete all compute nodes from virtual machine.
        
        Parameters
        ----------
            invalidate_case : bool
                'invalidate_case' child.
            delete_all_compute_nodes : bool
                'delete_all_compute_nodes' child.
        
        """

    def kill_node(self, compute_node: int, invalidate_case: bool):
        """
        'kill_node' command.
        
        Parameters
        ----------
            compute_node : int
                'compute_node' child.
            invalidate_case : bool
                'invalidate_case' child.
        
        """

    def spawn_node(self, hostname: str, username: str):
        """
        Spawn a compute node process on a specified machine.
        
        Parameters
        ----------
            hostname : str
                'hostname' child.
            username : str
                'username' child.
        
        """

    def load_hosts(self, host_file: str):
        """
        Read a hosts file.
        
        Parameters
        ----------
            host_file : str
                'host_file' child.
        
        """

    def save_hosts(self, host_file: str):
        """
        Write a hosts file.
        
        Parameters
        ----------
            host_file : str
                'host_file' child.
        
        """

