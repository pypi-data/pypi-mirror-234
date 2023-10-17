"""
flowdeploy.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains custom exceptions used for the FlowDeploy client.
"""


class FlowDeployException(OSError):
    """There was an unknown exception that occurred during your
    FlowDeploy job.
    """


class FlowDeployKeyError(FlowDeployException):
    """Invalid FlowDeploy auth key."""


class FlowDeployS3AccessError(FlowDeployException):
    """S3 input cannot be accessed by FlowDeploy."""


class FlowDeployJobError(FlowDeployException):
    """An error occurred when running the job instance."""
