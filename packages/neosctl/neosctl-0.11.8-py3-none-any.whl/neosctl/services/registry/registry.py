import typing
from uuid import UUID

import httpx
import typer

from neosctl import constant, util
from neosctl.services.registry import schema
from neosctl.util import process_response

app = typer.Typer()


ACCOUNT_ARG = typer.Option(None, help="Account override (root only).", callback=util.sanitize)


def _core_url(registry_api_url: str) -> str:
    return "{}/core".format(registry_api_url.rstrip("/"))


def _mesh_core_url(registry_api_url: str) -> str:
    return "{}/mesh/core".format(registry_api_url.rstrip("/"))


def _data_product_url(registry_api_url: str, postfix: str = "") -> str:
    return "{}/data_product{}".format(registry_api_url.rstrip("/"), postfix)


def _mesh_data_product_url(registry_api_url: str, identifier: str) -> str:
    return "{}/mesh/core/{}/data_product".format(registry_api_url.rstrip("/"), identifier)


@app.command(name="register-core")
def register_core(
    ctx: typer.Context,
    partition: str = typer.Argument(..., help="Core partition", callback=util.sanitize),
    name: str = typer.Argument(..., help="Core name", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
    *,
    private: bool = typer.Option(
        False,
        "--private",
        help="Limit visibility in mesh to core account.",
        callback=util.sanitize,
    ),
) -> None:
    """Register a core.

    Register a core to receive an identifier and access key for use in deployment.
    """

    @util.ensure_login
    def _request(ctx: typer.Context, rc: schema.RegisterCore) -> httpx.Response:
        return util.post(
            ctx,
            constant.REGISTRY,
            _core_url(ctx.obj.get_registry_api_url()),
            json=rc.model_dump(exclude_none=True),
            headers={"X-Partition": partition},
            account=account,
        )

    rc = schema.RegisterCore(name=name, public=not private)

    r = _request(ctx, rc)
    process_response(r)


@app.command(name="migrate-core")
def migrate_core(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    urn: str = typer.Option(..., help="Core urn", callback=util.sanitize),
    account: str = typer.Option(..., help="Account name", callback=util.sanitize),
) -> None:
    """Migrate a core out of root account.

    Migrate a core from `root` into an actual account.
    """

    @util.ensure_login
    def _request(ctx: typer.Context, mc: schema.MigrateCore) -> httpx.Response:
        return util.post(
            ctx,
            constant.REGISTRY,
            f"{_core_url(ctx.obj.get_registry_api_url())}/{identifier}/migrate",
            json=mc.model_dump(),
        )

    mc = schema.MigrateCore(
        urn=urn,
        account=account,
    )

    r = _request(ctx, mc)
    process_response(r)


@app.command(name="list-cores")
def list_cores(
    ctx: typer.Context,
) -> None:
    """List accessible cores."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _core_url(ctx.obj.get_registry_api_url()),
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="remove-core")
def remove_core(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Remove a registered core."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            constant.REGISTRY,
            f"{_core_url(ctx.obj.get_registry_api_url())}/{identifier}",
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="search")
def search_products(
    ctx: typer.Context,
    search_term: str = typer.Argument(..., callback=util.sanitize),
    *,
    keyword: bool = typer.Option(False, "--keyword/--hybrid", help="Search mode"),
) -> None:
    """Search published data products across cores."""

    @util.ensure_login
    def _request(ctx: typer.Context, search_term: str, keyword: bool) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _data_product_url(ctx.obj.get_registry_api_url(), "/search"),
            params={"search_term": search_term, "keyword_search": keyword},
        )

    r = _request(ctx, search_term, keyword)
    process_response(r)


@app.command(name="get-product")
def get_product(
    ctx: typer.Context,
    urn: str = typer.Argument(..., callback=util.sanitize),
) -> None:
    """Get data product details."""

    @util.ensure_login
    def _request(ctx: typer.Context, urn: str) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _data_product_url(ctx.obj.get_registry_api_url(), f"/urn/{urn}"),
        )

    r = _request(ctx, urn)
    process_response(r)


@app.command(name="upsert-contact")
def upsert_contact(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    user_id: UUID = typer.Option(..., help="Contact id"),
    role: str = typer.Option(..., help="Contact role"),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Add/Update a contact for a core."""

    @util.ensure_login
    def _request(ctx: typer.Context, c: schema.AddCoreContact) -> httpx.Response:
        return util.post(
            ctx,
            constant.REGISTRY,
            f"{_core_url(ctx.obj.get_registry_api_url())}/{identifier}/contact",
            json=c.model_dump(),
            account=account,
        )

    mc = schema.AddCoreContact(
        user_id=str(user_id),
        role=role,
    )

    r = _request(ctx, mc)
    process_response(r)


@app.command(name="remove-contact")
def remove_contact(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    user_id: UUID = typer.Option(..., help="Contact id"),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Remove a contact for a core."""

    @util.ensure_login
    def _request(ctx: typer.Context, c: schema.RemoveCoreContact) -> httpx.Response:
        return util.delete(
            ctx,
            constant.REGISTRY,
            f"{_core_url(ctx.obj.get_registry_api_url())}/{identifier}/contact",
            json=c.model_dump(),
            account=account,
        )

    mc = schema.RemoveCoreContact(
        user_id=str(user_id),
    )

    r = _request(ctx, mc)
    process_response(r)


@app.command(name="mesh-cores")
def mesh_cores(
    ctx: typer.Context,
    account: typing.Optional[str] = ACCOUNT_ARG,
    search: str = typer.Option(None, help="Search core name(s)", callback=util.sanitize),
) -> None:
    """List visible cores."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _mesh_core_url(ctx.obj.get_registry_api_url()),
            params={"search": search} if search else None,
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="mesh-core-products")
def mesh_core_products(
    ctx: typer.Context,
    identifier: str = typer.Option(..., help="Core identifier"),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """List visible products in a core."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _mesh_data_product_url(ctx.obj.get_registry_api_url(), identifier),
            account=account,
        )

    r = _request(ctx)
    process_response(r)
