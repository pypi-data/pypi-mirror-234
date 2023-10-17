from typing import List, Optional

import typer

from neosctl import util
from neosctl.services.gateway import entity

app = typer.Typer(name="data_system")


def _data_system_url(ctx: typer.Context) -> str:
    return "{}/v2/data_system".format(ctx.obj.get_gateway_api_url().rstrip("/"))


arg_generator = entity.EntityArgGenerator("Data System")


@app.command(name="create")
def create_entity(
    ctx: typer.Context,
    label: str = arg_generator.label,
    name: str = arg_generator.name,
    description: str = arg_generator.description,
    owner: Optional[str] = arg_generator.owner_optional,
    contacts: List[str] = arg_generator.contacts,
    links: List[str] = arg_generator.links,
) -> None:
    """Create data system."""
    entity.create_entity(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        label=label,
        name=name,
        description=description,
        owner=owner,
        contacts=contacts,
        links=links,
    )


@app.command(name="list")
def list_entities(ctx: typer.Context) -> None:
    """List data systems."""
    entity.list_entities(ctx=ctx, url=_data_system_url(ctx=ctx))


@app.command(name="get")
def get_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get data system."""
    entity.get_entity(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="delete")
def delete_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Delete data system."""
    entity.delete_entity(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="get-info")
def get_entity_info(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get data system info."""
    entity.get_entity_info(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="update")
def update_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    label: str = arg_generator.label,
    name: str = arg_generator.name,
    description: str = arg_generator.description,
) -> None:
    """Update data system."""
    entity.update_entity(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
        label=label,
        name=name,
        description=description,
    )


@app.command(name="update-info")
def update_entity_info(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    owner: str = arg_generator.owner,
    contacts: List[str] = arg_generator.contacts,
    links: List[str] = arg_generator.links,
) -> None:
    """Update data system info."""
    entity.update_entity_info(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
        owner=owner,
        contacts=contacts,
        links=links,
    )


@app.command(name="get-journal")
def get_entity_journal(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    page: int = typer.Option(1, "--page", "-p", help="Page number", callback=util.sanitize),
    per_page: int = typer.Option(25, "--per-page", "-pp", help="Number of items per page", callback=util.sanitize),
) -> None:
    """Get data system journal."""
    entity.get_entity_journal(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
        page=page,
        per_page=per_page,
    )


@app.command(name="update-journal")
def update_entity_journal(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    filepath: str = typer.Argument(..., help="Filepath to journal note payload", callback=util.sanitize),
) -> None:
    """Update data system journal."""
    entity.update_entity_journal(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
        filepath=filepath,
    )


@app.command(name="get-links")
def get_entity_links(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get data system links."""
    entity.get_entity_links(
        ctx=ctx,
        url=_data_system_url(ctx=ctx),
        identifier=identifier,
    )
