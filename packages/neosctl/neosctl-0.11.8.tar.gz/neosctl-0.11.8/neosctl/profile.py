import re
import typing

import click
import typer

from neosctl import schema, util
from neosctl.util import (
    exit_with_output,
    get_user_profile_section,
    prettify_json,
    remove_config,
    upsert_config,
    upsert_credential,
)

app = typer.Typer()


r = re.compile(r"http[s]?:\/\/.*")


def _validate_url(value: str) -> str:
    """Validate a given url is a valid url with schema."""
    m = r.match(value)
    if m is None:
        msg = f"Invalid url, must match pattern: `{r}`."
        raise click.UsageError(msg)
    return value


@app.command()
def init(
    ctx: typer.Context,
    *,
    hostname: typing.Optional[str] = typer.Option(None, "--host", "-h", callback=util.sanitize),
    gateway_api_url: typing.Optional[str] = typer.Option(None, "--gateway-api-url", "-g", callback=util.sanitize),
    registry_api_url: typing.Optional[str] = typer.Option(None, "--registry-api-url", "-r", callback=util.sanitize),
    iam_api_url: typing.Optional[str] = typer.Option(None, "--iam-api-url", "-i", callback=util.sanitize),
    storage_api_url: typing.Optional[str] = typer.Option(None, "--storage-api-url", "-s", callback=util.sanitize),
    username: typing.Optional[str] = typer.Option(None, "--username", "-u", callback=util.sanitize),
    account: typing.Optional[str] = typer.Option("root", "--account", "-a", callback=util.sanitize),
    ignore_tls: bool = typer.Option(
        False,
        "--ignore-tls",
        help="Ignore TLS errors (useful in local/development environments",
    ),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Don't ask for input, generate api values based on hostname.",
    ),
) -> None:
    """Initialise a profile.

    Create a profile that can be reused in later commands to define which
    services to interact with, and which user to interact as.

    Call `init` on an existing profile will update the existing profile.
    """
    typer.echo(f"Initialising [{ctx.obj.profile_name}] profile.")
    default_host = f"{hostname}/api/{{}}" if hostname else ""
    bare_host = hostname.replace("http://", "").replace("https://", "") if hostname else ""

    if non_interactive and not (hostname and username):
        raise exit_with_output(
            msg="\nError: --hostname/-h and --username/-u required for non-interactive mode.",
            exit_code=1,
        )

    if non_interactive:
        gateway_api_url = gateway_api_url or f"{hostname}/api/gateway"
        storage_api_url = storage_api_url or f"https://saas.{bare_host}"
        iam_api_url = iam_api_url or f"{hostname}/api/iam"
        registry_api_url = registry_api_url or f"{hostname}/api/registry"

    urls = {
        "gateway_api_url": gateway_api_url,
        "registry_api_url": registry_api_url,
        "iam_api_url": iam_api_url,
        "storage_api_url": storage_api_url,
    }
    for key, default, prompt in [
        ("gateway", ctx.obj.get_gateway_api_url(), "Gateway API url"),
        ("registry", ctx.obj.get_registry_api_url(), "Registry API url"),
        ("iam", ctx.obj.get_iam_api_url(), "IAM API url"),
        ("storage", ctx.obj.get_storage_api_url(), "Storage API url"),
    ]:
        url_key = f"{key}_api_url"
        url = urls[url_key]
        if url is None:
            urls[url_key] = typer.prompt(
                prompt,
                default=default or default_host.format(key),
                value_proc=_validate_url,
            )
        else:
            _validate_url(url)

    if username is None:
        kwargs = {}
        if ctx.obj.profile:
            kwargs["default"] = ctx.obj.profile.user
        username_input: str = typer.prompt(
            "Username",
            **kwargs,
        )
        username = username_input

    profile = schema.Profile(  # nosec: B106
        user=username,
        account=account,
        access_token="",
        refresh_token="",
        ignore_tls=ignore_tls,
        **urls,
    )

    upsert_config(ctx, profile)


@app.command()
def delete(
    ctx: typer.Context,
) -> None:
    """Delete a profile."""
    typer.confirm(f"Remove [{ctx.obj.profile_name}] profile", abort=True)
    remove_config(ctx)


@app.command()
def view(
    ctx: typer.Context,
) -> None:
    """View configuration for a profile."""
    profile = get_user_profile_section(ctx.obj.config, ctx.obj.profile_name)
    raise exit_with_output(
        msg=prettify_json({k: v for k, v in profile.items()}),  # noqa: C416
    )


@app.command()
def credentials(
    ctx: typer.Context,
    access_key_id: str,
    secret_access_key: str,
) -> None:
    """View configuration for a profile."""
    upsert_credential(ctx, access_key_id, secret_access_key)


@app.command(name="list")
def list_profiles(
    ctx: typer.Context,
) -> None:
    """List available profiles."""
    raise exit_with_output(
        msg=prettify_json(sorted(ctx.obj.config.sections())),
    )
