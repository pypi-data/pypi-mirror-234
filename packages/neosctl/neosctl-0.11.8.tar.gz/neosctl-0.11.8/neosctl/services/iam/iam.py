import typing
from uuid import UUID

import httpx
import typer

from neosctl import constant, util
from neosctl.services.iam import schema
from neosctl.util import process_response, user_profile_callback

app = typer.Typer(name=constant.IAM, callback=user_profile_callback)

account_app = typer.Typer(name="account")
user_app = typer.Typer(name="user")
policy_app = typer.Typer(name="policy")
group_app = typer.Typer(name="group")

app.add_typer(account_app, name="account", help="Manage accounts.")
app.add_typer(user_app, name="user", help="Manage users.")
app.add_typer(group_app, name="group", help="Manage groups.")
app.add_typer(policy_app, name="policy", help="Manage policies.")


ACCOUNT_ARG = typer.Option(None, help="Account override (root only).", callback=util.sanitize)


def _iam_url(iam_api_url: str, postfix: str = "") -> str:
    return "{}/{}".format(iam_api_url.rstrip("/"), postfix)


@account_app.command(name="create")
def create_account(
    ctx: typer.Context,
    display_name: str = typer.Option(..., "--display-name", "-d", help="Account display name."),
    name: str = typer.Option(..., "--name", "-n", help="Account name (used in urns)."),
    description: str = typer.Option(..., "--description", "--desc", help="Account description."),
    owner: str = typer.Option(..., "--owner", "-o", help="Account owner."),
) -> None:
    """Create a system account."""

    @util.ensure_login
    def _request(ctx: typer.Context, data: schema.CreateAccount) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "account"),
            json=data.model_dump(mode="json"),
        )

    data = schema.CreateAccount(
        display_name=display_name,
        name=name,
        description=description,
        owner=owner,
    )

    r = _request(ctx, data)
    process_response(r)


@account_app.command(name="list")
def list_accounts(
    ctx: typer.Context,
) -> None:
    """List system accounts."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "account"),
        )

    r = _request(ctx)
    process_response(r)


@policy_app.command(name="list")
def list_policies(
    ctx: typer.Context,
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(10, help="Page size number."),
    resource: typing.Optional[str] = typer.Option(None, help="Resource nrn.", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """List existing policies."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        params: typing.Dict[str, typing.Union[int, str]] = {"page": page, "page_size": page_size}
        if resource:
            params["resource"] = resource

        return util.get(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "policy/users"),
            params=params,
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@policy_app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Create an IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context, user_policy: schema.UserPolicy) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            json=user_policy.model_dump(mode="json"),
            account=account,
        )

    fp = util.get_file_location(filepath)
    user_policy_payload = util.load_json_file(fp, "policy")

    user_policy = schema.UserPolicy(**user_policy_payload)  # type: ignore[reportGeneralTypeIssues]

    r = _request(ctx, user_policy)
    process_response(r)


@policy_app.command(name="update")
def update_from_json(
    ctx: typer.Context,
    principal: str = typer.Argument(..., help="Principal uuid", callback=util.sanitize),
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Update an existing IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context, user_policy: schema.UserPolicy) -> httpx.Response:
        params = {"user_nrn": principal}
        return util.put(
            ctx,
            constant.IAM,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params=params,
            json=user_policy.model_dump(mode="json"),
            account=account,
        )

    fp = util.get_file_location(filepath)
    user_policy_payload = util.load_json_file(fp, "policy")

    user_policy = schema.UserPolicy(**user_policy_payload)  # type: ignore[reportGeneralTypeIssues]

    r = _request(ctx, user_policy)
    process_response(r)


@policy_app.command()
def delete(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Delete an existing IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        params = {"user_nrn": user_nrn}
        return util.delete(
            ctx,
            constant.IAM,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params=params,
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@policy_app.command()
def get(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Get an existing IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        params = {"user_nrn": user_nrn}
        return util.get(
            ctx,
            constant.IAM,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params=params,
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@user_app.command(name="create")
def create_user(
    ctx: typer.Context,
    username: str = typer.Option(..., "--username", "-u", callback=util.sanitize),
    email: str = typer.Option(..., "--email", "-e", callback=util.sanitize),
    first_name: str = typer.Option(..., "--first-name", "-f", callback=util.sanitize),
    last_name: str = typer.Option(..., "--last-name", "-l", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Create a keycloak user, and assign to account."""

    @util.ensure_login
    def _request(ctx: typer.Context, user: schema.CreateUser) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "user"),
            json=user.model_dump(mode="json"),
            account=account,
            timeout=30,
        )

    user = schema.CreateUser(
        enabled=True,
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    r = _request(ctx, user)
    process_response(r)


@user_app.command(name="create-key-pair")
def create_key_pair(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Create an access key_pair and assign to a user."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), f"user/{user_nrn}/key_pair"),
            account=account,
            timeout=30,
        )

    r = _request(ctx)
    process_response(r)


@user_app.command(name="list")
def list_users(
    ctx: typer.Context,
    search: str = typer.Option(None, help="Search term", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """List existing keycloak users.

    Filter by search term on username, first_name, last_name, or email.
    """

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        params = {"search": search} if search else None
        return util.get(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "users"),
            params=params,
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@user_app.command(name="permissions")
def user_permissions(
    ctx: typer.Context,
    username: str = typer.Option(None, help="Keycloak username", callback=util.sanitize),
    identifier: UUID = typer.Option(None, help="User or Group identifier", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """List existing keycloak user permissions."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        user_id = identifier

        if username:
            params = {"search": username}
            r = util.get(
                ctx,
                constant.IAM,
                _iam_url(ctx.obj.get_iam_api_url(), "users"),
                params={"search": username},
                account=account,
            )
            if r.status_code >= constant.BAD_REQUEST_CODE:
                process_response(r)

            data = r.json()
            # In case search term matches email/name of another user, filter for specific username
            user_id = next((user["id"] for user in data["users"] if user["username"] == username), None)

        if user_id is None:
            typer.echo("User not found.")
            raise typer.Exit(code=1)

        params = {"user_nrn": user_id}
        return util.get(
            ctx,
            constant.IAM,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params=params,
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@user_app.command(name="reset-password")
def reset_password(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="Keycloak user `username`", callback=util.sanitize),
) -> None:
    """Request a password reset for a user."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "user/password/reset"),
            params={"username": username},
        )

    r = _request(ctx)
    process_response(r)


@group_app.command(name="create")
def create_group(
    ctx: typer.Context,
    name: str = typer.Option(..., help="Group name", callback=util.sanitize),
    description: str = typer.Option(..., help="Group description", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Create an IAM group."""

    @util.ensure_login
    def _request(ctx: typer.Context, group: schema.CreateUpdateGroup) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "group"),
            json=group.model_dump(mode="json"),
            account=account,
        )

    group = schema.CreateUpdateGroup(name=name, description=description)

    r = _request(ctx, group)
    process_response(r)


@group_app.command(name="update")
def update_group(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    name: str = typer.Option(..., help="Group name", callback=util.sanitize),
    description: str = typer.Option(..., help="Group description", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Update an IAM group."""

    @util.ensure_login
    def _request(ctx: typer.Context, group: schema.CreateUpdateGroup) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), f"group/{identifier}"),
            json=group.model_dump(mode="json"),
            account=account,
        )

    group = schema.CreateUpdateGroup(name=name, description=description)

    r = _request(ctx, group)
    process_response(r)


@group_app.command(name="list")
def list_groups(
    ctx: typer.Context,
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """List IAM groups."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), "group"),
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@group_app.command(name="get")
def get_group(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Get an IAM group."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), f"group/{identifier}"),
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@group_app.command(name="delete")
def delete_group(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Delete an IAM group."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), f"group/{identifier}"),
            account=account,
        )

    r = _request(ctx)
    process_response(r)


@group_app.command(name="add-principals")
def add_principals(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    principals: typing.List[str] = typer.Option(
        ...,
        "--principal",
        "-p",
        help="Prinicpal identifiers",
        callback=util.sanitize,
    ),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Add principal(s) to an IAM group."""

    @util.ensure_login
    def _request(ctx: typer.Context, update: schema.Principals) -> httpx.Response:
        return util.post(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), f"group/{identifier}/principals"),
            json=update.model_dump(mode="json"),
            account=account,
        )

    update = schema.Principals(principals=principals)

    r = _request(ctx, update)
    process_response(r)


@group_app.command(name="remove-principals")
def remove_principals(
    ctx: typer.Context,
    identifier: UUID = typer.Argument(..., help="Group identifier", callback=util.sanitize),
    principals: typing.List[str] = typer.Option(
        ...,
        "--principal",
        "-p",
        help="Prinicpal identifiers",
        callback=util.sanitize,
    ),
    account: typing.Optional[str] = ACCOUNT_ARG,
) -> None:
    """Remove principal(s) from an IAM group."""

    @util.ensure_login
    def _request(ctx: typer.Context, update: schema.Principals) -> httpx.Response:
        return util.delete(
            ctx,
            constant.IAM,
            _iam_url(ctx.obj.get_iam_api_url(), f"group/{identifier}/principals"),
            json=update.model_dump(mode="json"),
            account=account,
        )

    update = schema.Principals(principals=principals)

    r = _request(ctx, update)
    process_response(r)
