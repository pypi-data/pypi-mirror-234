#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class simulation_reports:
    fluent_name = ...
    command_names = ...

    def list_simulation_reports(self, ):
        """
        List all report names.
        """

    def generate_simulation_report(self, report_name: str):
        """
        Generate a new simulation report or regenerate an existing simulation report with the provided name.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def view_simulation_report(self, report_name: str):
        """
        View a simulation report that has already been generated. In batch mode this will print the report's URL.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def export_simulation_report_as_pdf(self, report_name: str, file_name_path: str):
        """
        Export the provided simulation report as a PDF file.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            file_name_path : str
                'file_name_path' child.
        
        """

    def export_simulation_report_as_html(self, report_name: str, output_dir: str):
        """
        Export the provided simulation report as HTML.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            output_dir : str
                'output_dir' child.
        
        """

    def export_simulation_report_as_pptx(self, report_name: str, file_name_path: str):
        """
        Export the provided simulation report as a PPT file.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            file_name_path : str
                'file_name_path' child.
        
        """

    def write_simulation_report_names_to_file(self, file_path: str):
        """
        Write the list of currently generated report names to a txt file.
        
        Parameters
        ----------
            file_path : str
                'file_path' child.
        
        """

    def rename_simulation_report(self, report_name: str, new_report_name: str):
        """
        Rename a report which has already been generated.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            new_report_name : str
                'new_report_name' child.
        
        """

    def duplicate_simulation_report(self, report_name: str):
        """
        Duplicate the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def reset_report_to_defaults(self, report_name: str):
        """
        Reset all report settings to default for the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def delete_simulation_report(self, report_name: str):
        """
        Delete the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def write_simulation_report_template_file(self, file_name_path: str):
        """
        'write_simulation_report_template_file' command.
        
        Parameters
        ----------
            file_name_path : str
                'file_name_path' child.
        
        """

    def read_simulation_report_template_file(self, file_name_path: str):
        """
        Read a JSON template file with existing Simulation Report settings.
        
        Parameters
        ----------
            file_name_path : str
                'file_name_path' child.
        
        """

