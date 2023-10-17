import typer

from neosctl import constant, util
from neosctl.services.gateway import schema

app = typer.Typer(name="journal-note")


def _identified_journal_note_url(ctx: typer.Context, identifier: str) -> str:
    return "{}/v2/journal_note/{}".format(
        ctx.obj.get_gateway_api_url().rstrip("/"),
        identifier,
    )


IDENTIFIER_ARGUMENT = typer.Argument(..., help="Journal Note identifier", callback=util.sanitize)


@app.command(name="get")
def get_element(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
) -> None:
    """Get journal note."""
    util.get_and_process(
        ctx,
        constant.GATEWAY,
        _identified_journal_note_url(ctx, identifier),
    )


@app.command(name="update")
def update_element(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
    filepath: str = typer.Argument(..., help="Filepath to journal note payload", callback=util.sanitize),
) -> None:
    """Update journal note."""
    data = util.load_object(schema.UpdateJournalNote, filepath, "journal_note")
    util.put_and_process(
        ctx,
        constant.GATEWAY,
        _identified_journal_note_url(ctx, identifier),
        json=data.model_dump(by_alias=True),
    )


@app.command(name="delete")
def delete_element(
    ctx: typer.Context,
    identifier: str = IDENTIFIER_ARGUMENT,
) -> None:
    """Delete journal note."""
    util.delete_and_process(
        ctx,
        constant.GATEWAY,
        _identified_journal_note_url(ctx, identifier),
    )
