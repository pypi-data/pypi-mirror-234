import json
import subprocess

import typer
from typing_extensions import Annotated
from flowdeploy import nextflow, set_key

app = typer.Typer(pretty_exceptions_show_locals=False)


def parse_input_file(path):
    if path:
        with open(path, 'r') as file:
            return json.load(file)
    return None


@app.command()
def run(
    pipeline: Annotated[str, typer.Argument(help="The name of the pipeline")],
    outdir: Annotated[
        str, typer.Option('--outdir', '-o', help="Where to place pipeline outputs. Must be a FlowDeploy file path.")
    ],
    pipeline_version: Annotated[str, typer.Option('--version', '-v', help="The version of the pipeline")],
    input_file: Annotated[
        str, typer.Option('--input-file', '-i', help="Path to a json file with the input(s) defined")
    ] = None,
    cli_args: Annotated[
        str, typer.Option(help="Raw command line args to pass to the pipeline (must be in quotes)")
    ] = '',
    export_location: Annotated[
        str, typer.Option(help="Where to export (i.e. upload) the output directory. S3 only.")
    ] = None,
    profile_string: Annotated[
        str,
        typer.Option(
            '--profile',
            help="Workflow manager configuration profiles. Multiple profiles can be comma separated when supported."
        )
    ] = None,
    run_location: Annotated[
        str, typer.Option(help="A FlowDeploy path to use as the working directory for the pipeline.")
    ] = None,
    is_async: Annotated[
        bool,
        typer.Option("--is-async", help="Exits immediately after spawning the FlowDeploy instance if set")
    ] = False,
    flowdeploy_key: Annotated[
        str,
        typer.Option(help="FlowDeploy API key to authenticate the run (can also be set in the environment)")
    ] = None,
):
    """
    Runs a pipeline with FlowDeploy
    """
    if flowdeploy_key:
        set_key(flowdeploy_key)
    inputs = parse_input_file(input_file)
    profiles = None
    if profile_string:
        profiles = list(filter(lambda profile: profile != '', profile_string.split(',')))
    nextflow(
        pipeline=pipeline,
        outdir=outdir,
        pipeline_version=pipeline_version,
        inputs=inputs,
        cli_args=cli_args,
        export_location=export_location,
        profiles=profiles,
        run_location=run_location,
        is_async=is_async,
        cli=True,
    )


@app.command('set-key')
def set_flowdeploy_key(
    flowdeploy_key: Annotated[str, typer.Argument(help="Sets your FlowDeploy key in your environment")],
    config_file: Annotated[
        str, typer.Option('--config', '-c', help="Path to the config file to set the key in")
    ] = None,
):
    """
    Appends FLOWDEPLOY_KEY to the end of the shell environment config file.
    Defaults to '~/.zshenv' on macOS and '~/.bashrc' on Linux.
    """
    config_location = config_file
    try:
        if not config_file:
            uname = subprocess.run("uname", capture_output=True, shell=True).stdout.strip().decode('utf-8')
            config_location = '~/.zshenv' if uname == 'Darwin' else '~/.bashrc'
        subprocess.run(f'echo "export FLOWDEPLOY_KEY={flowdeploy_key}" >> {config_location}', text=True, shell=True)\
            .check_returncode()
        success_message = f"Key is now set in {config_location}. " \
                          f"Restart your terminal or run `source {config_location}` to use the key."
        print(success_message)
    except subprocess.CalledProcessError as err:
        raise ValueError(f"Failed to set key in {config_location}\n", err.output)
