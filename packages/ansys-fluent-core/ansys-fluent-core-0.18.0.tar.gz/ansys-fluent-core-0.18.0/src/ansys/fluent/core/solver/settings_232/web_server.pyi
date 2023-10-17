#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class web_server:
    fluent_name = ...
    command_names = ...

    def start(self, session_name: str, port: int, port_span: int, job_service_url: str):
        """
        Start the web server.
        
        Parameters
        ----------
            session_name : str
                Name for the web server.
            port : int
                Listening port for the web server.
            port_span : int
                Number of ports to try starting from given 'port' for the web server.
            job_service_url : str
                Job service URL to register Fluent.
        
        """

    def stop(self, ):
        """
        Stop the web server.
        """

    def print_server_info(self, ):
        """
        Print the web server information.
        """

    def get_server_info(self, ):
        """
        Get the web server information.
        """

