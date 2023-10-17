from typing import Optional

import typer

from neosctl import constant, util
from neosctl.services.gateway import schema

app = typer.Typer(name="output")


def _tag_url(ctx: typer.Context) -> str:
    return "{}/v2/tag".format(ctx.obj.get_gateway_api_url().rstrip("/"))


NAME_ARGUMENT = typer.Argument(..., help="Tag name")
SCOPE_ARGUMENT = typer.Argument(..., help="Tag scope")


@app.command(name="list")
def list_elements(
    ctx: typer.Context,
    scope: schema.TagScope = SCOPE_ARGUMENT,
    *,
    system_defined: bool = typer.Option(False, "--system-defined", "-s", help="System defined"),
    tag_filter: Optional[str] = typer.Option(None, "--filter", "-f", help="Filter query"),
) -> None:
    """List tags."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        _tag_url(ctx),
        params={
            "scope": scope.value,
            "system_defined": system_defined,
            "tag_filter": tag_filter,
        },
    )


@app.command(name="create")
def create_element(
    ctx: typer.Context,
    name: str = NAME_ARGUMENT,
    scope: schema.TagScope = SCOPE_ARGUMENT,
) -> None:
    """Create new tag."""
    data = schema.UpdateTag(
        tag=name,
        scope=scope.value,
    )

    util.post_and_process(
        ctx,
        constant.GATEWAY,
        _tag_url(ctx),
        json=data.model_dump(by_alias=True),
    )


@app.command(name="delete")
def delete_element(
    ctx: typer.Context,
    name: str = NAME_ARGUMENT,
    scope: schema.TagScope = SCOPE_ARGUMENT,
) -> None:
    """Delete tag."""
    data = schema.UpdateTag(
        tag=name,
        scope=scope.value,
    )
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        _tag_url(ctx),
        json=data.model_dump(by_alias=True),
    )
