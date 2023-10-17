import click

from montecarlodata.agents.agent import AgentService
from montecarlodata.agents.fields import (
    DATA_STORE_AGENT,
    GCS,
    S3,
    GCP,
    AWS,
    AWS_ASSUMABLE_ROLE,
    GCP_JSON_SERVICE_ACCOUNT_KEY,
)
from montecarlodata.common.commands import DISAMBIGUATE_DC_OPTIONS
from montecarlodata.tools import add_common_options


@click.group(help="Manage a Monte Carlo Agent.")
def agents():
    """
    Group for any Agent related subcommands
    """
    pass


@agents.command(help="Register a Data Store Agent with remote S3 bucket.")
@click.pass_obj
@click.option(
    "--assumable-role",
    help="ARN of AWS assumable role.",
    required=True,
)
@click.option(
    "--bucket-name",
    help="Name of S3 bucket for data store.",
    required=True,
)
@click.option(
    "--external-id",
    help="AWS External ID.",
    required=False,
)
@add_common_options(DISAMBIGUATE_DC_OPTIONS)
def register_s3_store(ctx, bucket_name, **kwargs):
    AgentService(config=ctx["config"]).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=AWS,
        storage=S3,
        auth_type=AWS_ASSUMABLE_ROLE,
        endpoint=bucket_name,
        **kwargs,
    )


@agents.command(help="Register a Data Store Agent with Google Cloud Storage.")
@click.pass_obj
@click.option(
    "--key-file",
    help="JSON Key file if auth type is GCP JSON service account key.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--bucket-name",
    help="Name of GCS bucket for data store.",
    required=True,
)
@add_common_options(DISAMBIGUATE_DC_OPTIONS)
def register_gcs_store(ctx, bucket_name, **kwargs):
    AgentService(config=ctx["config"]).create_agent(
        agent_type=DATA_STORE_AGENT,
        platform=GCP,
        storage=GCS,
        auth_type=GCP_JSON_SERVICE_ACCOUNT_KEY,
        endpoint=bucket_name,
        **kwargs,
    )


@agents.command(help="Deregister an Agent.")
@click.pass_obj
@click.option("--agent-id", help="UUID of Agent to deregister.", required=True)
def deregister(ctx, agent_id):
    """
    Deregister an Agent (deletes AgentModel from monolith)
    """
    AgentService(config=ctx["config"]).delete_agent(agent_id)


@agents.command(help="List all agents in account.", name="list")
@click.pass_obj
def list_agents(ctx):
    """
    List all Agents in account
    """
    AgentService(config=ctx["config"]).echo_agents()
