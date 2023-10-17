#!/usr/bin/env python

import click
import asyncio
import re
import pandas as pd
import tabulate
import terrascope.cli.lib.workflow as wf
import terrascope.cli.lib.utils as tsu
from terrascope.cli.lib.aliased_group import AliasedSuperGroup, AliasedGroup


@click.command(cls=AliasedGroup, help='Data source command group')
@click.pass_context
def source(ctx):
    pass


@source.command('get')
@click.pass_context
@click.option('-n', '--source_name', type=str)
def data_source_get(ctx, source_name):

    wf.check_environment_complete(raise_on_failure=True)

    data_sources = asyncio.run(wf.list_data_sources())

    data = []
    for data_source in data_sources:
        data_source = tsu.protobuf_to_dict(data_source)
        if re.search(source_name, data_source['id']):
            data.append(data_source)
    df = pd.DataFrame(data)
    click.secho("Supported Data Sources:", fg='cyan')
    click.echo(tabulate.tabulate(df.T, maxcolwidths=[None, 40]))


@source.command('list')
@click.pass_context
def data_source_list(ctx):

    wf.check_environment_complete(raise_on_failure=True)

    data_sources = asyncio.run(wf.list_data_sources())

    data = []
    for data_source in data_sources:
        data.append(tsu.protobuf_to_dict(data_source))
    df = pd.DataFrame(data)
    click.secho("Supported Data Sources:", fg='cyan')
    click.echo(df[['id', 'name', 'data_types']])


@click.command(cls=AliasedGroup, help='Data type command group')
@click.pass_context
def type(ctx):
    pass


@type.command('get')
@click.pass_context
@click.option('-n', '--type_name', type=str)
def data_type_get(ctx, type_name):

    wf.check_environment_complete(raise_on_failure=True)

    data_types = asyncio.run(wf.list_data_types())

    data = []
    for data_type in data_types:
        data_type = tsu.protobuf_to_dict(data_type)
        if re.search(type_name, data_type['name']):
            data.append(data_type)
    df = pd.DataFrame(data)

    click.secho("Supported Data Types:", fg='cyan')
    click.echo(tabulate.tabulate(df.T, maxcolwidths=[None, 40]))


@type.command('list')
@click.pass_context
def data_type_list(ctx):

    wf.check_environment_complete(raise_on_failure=True)

    data_types = asyncio.run(wf.list_data_types())

    data = []
    for data_type in data_types:
        data.append(tsu.protobuf_to_dict(data_type))
    df = pd.DataFrame(data)
    click.secho("Supported Data Types:", fg='cyan')
    click.echo(df)


@click.command(cls=AliasedSuperGroup, help="'data' super group")
@click.pass_context
def data(ctx):
    pass


data.add_command(source)
data.add_command(type)
