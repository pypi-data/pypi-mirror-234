#!/usr/bin/env python

import click
import asyncio
import os
import terrascope.cli.lib.workflow as wf
import terrascope.cli.lib.utils as tsu
from terrascope.cli.lib.aliased_group import AliasedGroup


@click.command(cls=AliasedGroup, help="Analysis 'computation' command group")
@click.pass_context
def computation(ctx):
    pass


@computation.command('get')
@click.pass_context
@click.option('-iP', '--analysis_computation_id', type=str)
def analysis_computation_get(ctx, analysis_computation_id):

    wf.check_environment_complete(raise_on_failure=True)

    analysis_computation_infos = asyncio.run(
        wf.get_analysis_computation_info()
    )

    for analysis_computation_info in analysis_computation_infos:
        info = tsu.protobuf_to_dict(analysis_computation_info)

        # if they asked for a specific one, just print that.  otherwise print all.
        if (analysis_computation_id is None) or \
           (analysis_computation_id and analysis_computation_id == info['id']):
            click.secho(f"analysis_computation_id: {info['id']}", fg='cyan')
            for k, v in info.items():
                click.echo(f"--> {k:20s} {v}")


@computation.command('create')
@click.pass_context
@click.option('-iC', '--analysis_config_id', type=str)
@click.option('--dry_run', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
@click.option('-it', '--toi_id', type=str)
@click.option('-ia', '--aoi_collection_id', type=str)
def analysis_computation_create(
        ctx,
        analysis_config_id,
        dry_run,
        verbose,
        toi_id,
        aoi_collection_id,
):

    wf.check_environment_complete(raise_on_failure=True)

    click.echo("Using the following information:")
    click.echo(f"--> analysis_config_id:       {analysis_config_id}")
    click.echo(f"--> toi_id:                   {toi_id}")
    click.echo(f"--> aoi_collection_id:        {aoi_collection_id}")

    if not dry_run:

        computation_id = asyncio.run(
            wf.create_analysis_computation(
                analysis_config_id,
                toi_id,
                aoi_collection_id,
            )
        )
        click.echo(f"computation_id: {computation_id}")


@computation.command('create_scratch')
@click.pass_context
@click.option('-iC', '--analysis_config_id', type=str)
@click.option('-s', '--start_date', type=str)
@click.option('-e', '--end_date', type=str)
@click.option('-af', '--aoi_file', type=str)
@click.option('-d', '--date_format', type=str, default='%Y-%m-%d')
@click.option('-f', '--frequency', type=click.IntRange(min=2, max=3, clamp=False), default=3,
              help="HOURLY=2, DAILY=3")
@click.option('--dry_run', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
def analysis_computation_create_scratch(
        ctx,
        analysis_config_id,
        start_date,
        end_date,
        aoi_file,
        date_format,
        frequency,
        dry_run,
        verbose,
):

    wf.check_environment_complete(raise_on_failure=True)
    click.echo("Using the following information:")
    click.echo(f"--> analysis_config_id:       {analysis_config_id}")
    click.echo(f"--> start_date:               {start_date}")
    click.echo(f"--> end_date:                 {end_date}")
    click.echo(f"--> aoi_file:                 {aoi_file}")
    click.echo(f"--> date_format:              {date_format}")
    click.echo(f"--> frequency:                {frequency}")

    if not dry_run:

        computation_id = asyncio.run(
            wf.create_analysis_computation_aoi_toi(
                analysis_config_id,
                start_date,
                end_date,
                aoi_file,
                date_format=date_format,
                frequency=frequency,
            )
        )

        click.echo(f"computation_id: {computation_id}")


@computation.command('run')
@click.pass_context
@click.option('-iP', '--analysis_computation_id', type=str)
@click.option('--dry_run', is_flag=True)
def analysis_computation_run(ctx, analysis_computation_id, dry_run):

    wf.check_environment_complete(raise_on_failure=True)
    if not dry_run:
        asyncio.run(wf.run_analysis_computations([analysis_computation_id]))


@computation.command('download')
@click.pass_context
@click.option('-iP', '--analysis_computation_id', type=str)
@click.option('-o', '--output_zip_file', type=str)
@click.option('--dry_run', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
@click.option('-c', '--clobber', is_flag=True, help="Overwrite existing output")
def analysis_computationf_download(
        ctx,
        analysis_computation_id,
        output_zip_file,
        dry_run,
        verbose,
        clobber,
):

    wf.check_environment_complete(raise_on_failure=True)

    if os.path.exists(output_zip_file):
        if not clobber:
            click.secho(f"File: {output_zip_file} exists. Run with '-c' to overwrite.  Exiting.", fg='red')
            raise RuntimeError("Output file already exists.")
        else:
            click.secho(f"File: {output_zip_file} exists.  I'm removing it.", fg='yellow')
            os.remove(output_zip_file)

    # we need an algo computation_id to download ... have to look up that final comp node's id.
    analysis_computation_infos = asyncio.run(wf.get_analysis_computation_info())
    algo_computation_id = None
    for analysis_computation_info in analysis_computation_infos:
        info = tsu.protobuf_to_dict(analysis_computation_info)
        if analysis_computation_id == info['id']:
            algo_computation_id = info['computation_nodes'][-1]['computation_id']
            break

    if algo_computation_id is None:
        raise RuntimeError(f'Could not find the algorithm_computation_id for {analysis_computation_id}')

    # get the computation_id first
    asyncio.run(wf.download_algorithm_computation_results(algo_computation_id, output_zip_file))

    click.echo(f"File {output_zip_file} ", nl=False)
    if not os.path.exists(output_zip_file):
        click.secho("NOT written", fg='red')
    else:
        click.secho("written.", fg='green')
