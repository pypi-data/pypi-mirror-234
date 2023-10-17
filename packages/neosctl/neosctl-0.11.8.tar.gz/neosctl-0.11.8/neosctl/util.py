import asyncio
import configparser
import json
import logging
import pathlib
import re
import sys
import typing

import click
import httpx
import pydantic
import typer
from neos_common.authorization.signer import KeyPair
from neos_common.client import base
from neos_common.error import HttpException
from pygments import formatters, highlight, lexers

from neosctl import constant, schema

logger = logging.getLogger("neosctl.error")

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


def dumps_formatted_json(payload: typing.Union[typing.Dict, typing.List]) -> str:
    """Dump formatted json.

    json.dump provided payload with indent 2 and sorted keys.
    """
    return json.dumps(payload, indent=2, sort_keys=True)


def prettify_json(payload: typing.Union[typing.Dict, typing.List]) -> str:
    """Dump formatted json with colour highlighting."""
    return highlight(dumps_formatted_json(payload), lexers.JsonLexer(), formatters.TerminalFormatter())


def is_success_response(response: httpx.Response) -> bool:
    """Check if a response is `successful`."""
    if constant.SUCCESS_CODE <= response.status_code < constant.REDIRECT_CODE:
        return True
    return False


def exit_with_output(msg: str, exit_code: int = 0) -> typer.Exit:
    """Render output to terminal and exit."""
    typer.echo(msg)

    return typer.Exit(exit_code)


def process_response(
    response: httpx.Response,
    render_callable: typing.Callable[[typing.Union[typing.Dict, typing.List]], str] = prettify_json,
) -> None:
    """Process a server response, render the output and exit."""
    exit_code = 0
    try:
        data = response.json()
        if response.status_code >= constant.BAD_REQUEST_CODE:
            exit_code = 1
            message = prettify_json(data)
        else:
            message = render_callable(data)
    except Exception:
        logger.info(response.content)
        logger.exception("Failure to parse response.")
        exit_code = 1
        message = "Unable to parse response."

    raise exit_with_output(
        msg=message,
        exit_code=exit_code,
    )


def read_config_dotfile() -> configparser.ConfigParser:
    """Read in `.neosctl/profile` configuration file and parse."""
    c = configparser.ConfigParser()
    if constant.ROOT_FILEPATH.is_file():
        # Move legacy profiles into `~/.neosctl folder`
        legacy = pathlib.Path(str(constant.ROOT_FILEPATH))
        backup = pathlib.Path(f"{constant.ROOT_FILEPATH}.bak")
        legacy.rename(str(backup))
        constant.ROOT_FILEPATH.mkdir()
        backup.rename(str(constant.PROFILE_FILEPATH))
    constant.ROOT_FILEPATH.mkdir(exist_ok=True)
    c.read(constant.PROFILE_FILEPATH)
    return c


def read_credential_dotfile() -> configparser.ConfigParser:
    """Read in `.neosctl/credential` configuration file and parse."""
    c = configparser.ConfigParser()
    c.read(constant.CREDENTIAL_FILEPATH)
    return c


def get_optional_user_profile_section(
    c: configparser.ConfigParser,
    profile_name: str,
) -> typing.Optional[configparser.SectionProxy]:
    """Get profile from neosctl configuration.

    Returns:
    -------
    Return configparser.SectionProxy if found, or None.
    """
    try:
        return c[profile_name]
    except KeyError:
        return None


def get_user_profile_section(c: configparser.ConfigParser, profile_name: str) -> configparser.SectionProxy:
    """Get profile from neosctl configuration.

    If profile is not found exit cli.

    Returns:
    -------
    configparser.SectionProxy for the requested profile.
    """
    try:
        return c[profile_name]
    except KeyError:
        pass

    raise exit_with_output(
        msg=f"Profile {profile_name} not found.",
        exit_code=1,
    )


def get_user_credential(
    c: configparser.ConfigParser,
    profile_name: str,
    *,
    optional: bool = False,
) -> typing.Union[schema.Credential, None]:
    """Get profile from neosctl credentials.

    If profile is not found exit cli.

    Returns:
    -------
    schema.Credential for the requested profile.
    """
    try:
        return schema.Credential(**c[profile_name])
    except KeyError:
        pass

    if not optional:
        raise exit_with_output(
            msg=f"Profile {profile_name} not configured with credentials.",
            exit_code=1,
        )
    return None


def _auth_url(iam_api_url: str) -> str:
    return "{}".format(iam_api_url.rstrip("/"))


def check_refresh_token_exists(ctx: typer.Context) -> bool:
    """Check if refresh token exists."""
    if not ctx.obj.profile.refresh_token:  # nosec: B105
        raise exit_with_output(
            msg=f"You need to login. Run neosctl -p {ctx.obj.profile_name} auth login",
            exit_code=1,
        )

    return True


def _refresh_token(ctx: typer.Context) -> httpx.Response:
    check_profile_exists(ctx)
    check_refresh_token_exists(ctx)

    r = post(
        ctx,
        constant.IAM,
        f"{_auth_url(ctx.obj.get_iam_api_url())}/refresh",
        json={"refresh_token": ctx.obj.profile.refresh_token},
    )

    if not is_success_response(r):
        process_response(r)

    upsert_config(ctx, update_profile(ctx, schema.Auth(**r.json())))

    return r


P = ParamSpec("P")


def ensure_login(method: typing.Callable[P, httpx.Response]) -> typing.Callable[P, httpx.Response]:
    """Capture authentication errors and retry requests.

    On request failure check if the response is a 401, and attempt to refresh the access_token.
    Retry the request with refreshed token, on subsequent failure, return.
    """

    def check_access_token(*args: P.args, **kwargs: P.kwargs) -> httpx.Response:
        ctx = args[0]
        if not isinstance(ctx, (typer.Context, click.Context)):
            # Developer reminder
            msg = "First argument should be click.Context instance"
            raise TypeError(msg)

        r = method(*args, **kwargs)

        check_profile_exists(ctx)

        # Try to refresh token
        # Confirm it is a token invalid 401, registry not configured mistriggers this flow.
        if r.status_code == constant.UNAUTHORISED_CODE:
            data = r.json()
            if "code" in data and data["code"].startswith("A0"):
                _refresh_token(ctx)

                # Refresh the context
                c = read_config_dotfile()
                ctx.obj.config = c
                ctx.obj.profile = get_user_profile(c, ctx.obj.profile_name)

                r = method(*args, **kwargs)

        return r

    return check_access_token


def update_profile(
    ctx: typer.Context,
    auth: schema.Auth = schema.Auth(),
) -> schema.Profile:
    """Update user profile."""
    return schema.Profile(
        gateway_api_url=ctx.obj.gateway_api_url,
        registry_api_url=ctx.obj.registry_api_url,
        iam_api_url=ctx.obj.iam_api_url,
        storage_api_url=ctx.obj.storage_api_url,
        user=ctx.obj.profile.user,
        access_token=auth.access_token,
        refresh_token=auth.refresh_token,
        ignore_tls=ctx.obj.profile.ignore_tls,
    )


def get_user_profile(
    c: configparser.ConfigParser,
    profile_name: str,
    *,
    allow_missing: bool = False,
) -> typing.Optional[typing.Union[schema.Profile, schema.OptionalProfile]]:
    """Get user profile.

    If allow_missing if False and the profile is not found, the cli will exit with an error output.
    """
    if allow_missing:
        profile_config = get_optional_user_profile_section(c, profile_name)
    else:
        profile_config = get_user_profile_section(c, profile_name)

    if profile_config:
        try:
            return schema.Profile(**profile_config)
        except pydantic.ValidationError as e:
            required_fields = [str(err["loc"][0]) for err in e.errors() if err["msg"] == "field required"]
            raise exit_with_output(  # noqa: TRY200, B904
                msg=("Profile dotfile doesn't include fields:\n  {}\nUse neosctl -p {} profile init").format(
                    "\n  ".join(required_fields),
                    profile_name,
                ),
                exit_code=1,
            )
    return None


def bearer(ctx: typer.Context) -> typing.Optional[typing.Dict]:
    """Generate bearer authorization header."""
    if not (ctx.obj.profile and ctx.obj.profile.access_token):  # nosec: B105
        return None

    return {"Authorization": f"Bearer {ctx.obj.profile.access_token}"}


def check_profile_exists(ctx: typer.Context) -> bool:
    """Check if a profile exists in neosctl configuration or exit."""
    if not ctx.obj.profile:
        raise exit_with_output(
            msg=f"Profile not found! Run neosctl -p {ctx.obj.profile_name} profile init",
            exit_code=1,
        )

    return True


def upsert_config(
    ctx: typer.Context,
    profile: schema.Profile,
) -> configparser.ConfigParser:
    """Update neosctl configuration profile in place."""
    ctx.obj.config[ctx.obj.profile_name] = profile.model_dump()

    with constant.PROFILE_FILEPATH.open("w") as profile_file:
        ctx.obj.config.write(profile_file)

    return ctx.obj.config


def upsert_credential(
    ctx: typer.Context,
    access_key_id: str,
    secret_access_key: str,
) -> None:
    """Update neosctl credential profile in place."""
    ctx.obj.credential[ctx.obj.profile_name] = {"access_key_id": access_key_id, "secret_access_key": secret_access_key}

    with constant.CREDENTIAL_FILEPATH.open("w") as profile_file:
        ctx.obj.credential.write(profile_file)


def remove_config(
    ctx: typer.Context,
) -> configparser.ConfigParser:
    """Remove a profile from neosctl configuration."""
    if not ctx.obj.config.remove_section(ctx.obj.profile_name):
        raise exit_with_output(
            msg=f"Can not remove {ctx.obj.profile_name} profile, profile not found.",
            exit_code=1,
        )
    ctx.obj.credential.remove_section(ctx.obj.profile_name)

    with constant.PROFILE_FILEPATH.open("w") as profile_file:
        ctx.obj.config.write(profile_file)

    with constant.CREDENTIAL_FILEPATH.open("w") as credential_file:
        ctx.obj.credential.write(credential_file)

    return ctx.obj.config


def get_file_location(filepath: str) -> pathlib.Path:
    """Get a Path for the provided filepath, exit if not found."""
    fp = pathlib.Path(filepath)
    if not fp.exists():
        raise exit_with_output(
            msg=f"Can not find file: {fp}",
            exit_code=1,
        )
    return fp


def load_json_file(fp: pathlib.Path, content_type: str) -> typing.Union[typing.Dict, typing.List]:
    """Load contents of json file, exit if not found."""
    with fp.open() as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            logger.exception("Error loading json file.")
            raise exit_with_output(  # noqa: TRY200, B904
                msg=f"Invalid {content_type} file, must be json format.",
                exit_code=1,
            )
            return []  # never reached as raise exit_with_output, but it makes type checker happy

    return data


T = typing.TypeVar("T", bound=pydantic.BaseModel)


def load_object(t: typing.Type[T], filepath: str, file_description: str) -> T:
    """Trying to read and parse JSON file into the given data type."""
    fp = get_file_location(filepath)
    obj = load_json_file(fp, file_description)
    if not isinstance(obj, dict):
        raise exit_with_output(
            msg=f"Require a json file containing an object, `{type(obj)}` provided.",
            exit_code=1,
        )
    try:
        return t(**obj)
    except pydantic.ValidationError as e:
        logger.exception("Error loading json file.")
        raise exit_with_output(
            msg=str(e),
            exit_code=1,
        ) from e


class GenericHttpClient(base.NeosClient):
    """Generic HTTP client supporting Bearer and NEOS-HMAC-SHA256 auth."""

    def __init__(  # noqa: D107
        self,
        service: str,
        token: typing.Union[str, None],
        key_pair: typing.Union[KeyPair, None],
    ) -> None:
        assert token is not None or key_pair is not None

        self._service = service
        self._token = token
        self._key_pair = key_pair

    @property
    def service_name(self) -> str:
        """Service name, used in signed scope."""
        return self._service

    @property
    def token(self) -> typing.Union[str, None]:
        """Bearer token, if provided."""
        return self._token

    @property
    def key_pair(self) -> typing.Union[KeyPair, None]:
        """Signing keypair, if provided."""
        return self._key_pair

    def request(
        self,
        url: str,
        method: base.Method,
        params: typing.Union[dict, None] = None,
        headers: typing.Union[dict, None] = None,
        json: typing.Union[dict, None] = None,
        **kwargs,  # noqa: ANN003
    ) -> httpx.Response:
        """Proxy for httpx requests."""
        return asyncio.run(self._request(url, method, params, headers, json, **kwargs))


def _request(ctx: typer.Context, method: str, service: str, url: str, **kwargs: ...) -> httpx.Response:
    credential = get_user_credential(ctx.obj.credential, ctx.obj.profile_name, optional=True)
    bearer = ctx.obj.profile.access_token if credential is None else None
    c = GenericHttpClient(
        service=service,
        token=bearer,
        key_pair=KeyPair(credential.access_key_id, credential.secret_access_key, "ksa") if credential else None,
    )

    headers = kwargs.pop("headers", None) or {}
    headers_, params_ = extract_account(ctx, account=kwargs.pop("account", None))
    headers_["X-Partition"] = "ksa"
    headers.update(headers_)

    params = kwargs.pop("params", None) or {}
    params.update(params_ or {})

    try:
        return c.request(
            url,
            base.Method[method],
            verify=not ctx.obj.profile.ignore_tls,
            params=params,
            headers=headers,
            **kwargs,
        )
    except HttpException as e:
        logger.exception("Request failed.")
        raise exit_with_output(
            msg=f"{service.title()} {method} request to {url} failed ({e.status}). [{e.code}]",
            exit_code=1,
        ) from e


def _request_and_process(ctx: typer.Context, method: str, service: str, url: str, **kwargs: ...) -> None:
    @ensure_login
    def internal_request(context: typer.Context) -> httpx.Response:
        return _request(context, method, service, url, **kwargs)

    response = internal_request(ctx)
    process_response(response)


def get_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process GET request."""
    _request_and_process(ctx, "GET", service, url, **kwargs)


def post_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process POST request."""
    _request_and_process(ctx, "POST", service, url, **kwargs)


def put_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process PUT request."""
    _request_and_process(ctx, "PUT", service, url, **kwargs)


def delete_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process DELETE request."""
    _request_and_process(ctx, "DELETE", service, url, **kwargs)


def patch_and_process(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> None:
    """Execute and process PATCH request."""
    _request_and_process(ctx, "PATCH", service, url, **kwargs)


def get(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a GET request."""
    return _request(ctx, "GET", service, url, **kwargs)


def post(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a POST request."""
    return _request(ctx, "POST", service, url, **kwargs)


def put(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a PUT request."""
    return _request(ctx, "PUT", service, url, **kwargs)


def delete(ctx: typer.Context, service: str, url: str, **kwargs: ...) -> httpx.Response:
    """Execute a DELETE request."""
    return _request(ctx, "DELETE", service, url, **kwargs)


def sanitize(
    ctx: typer.Context,  # noqa: ARG001
    param: click.Parameter,  # noqa: ARG001
    value: typing.Optional[str],
) -> typing.Optional[str]:
    """Parameter's sanitize callback."""
    if value and isinstance(value, str):
        return value.rstrip("\r\n")

    return value


def validate_string_not_empty(
    ctx: typer.Context,
    param: click.Parameter,
    value: str,
) -> str:
    """String validation callback."""
    value = value.strip()

    if not value:
        message = "Value must be a non-empty string."
        raise typer.BadParameter(message, ctx=ctx, param=param)

    return value


def validate_strings_are_not_empty(
    ctx: typer.Context,
    param: click.Parameter,
    values: typing.List[str],
) -> typing.List[str]:
    """List of strings validation callback."""
    return [validate_string_not_empty(ctx, param, value) for value in values]


def validate_regex(
    pattern: str,
) -> typing.Callable[[typer.Context, click.Parameter, str], str]:
    """Regex validation callback."""

    def factory(
        ctx: typer.Context,
        param: click.Parameter,
        value: str,
    ) -> str:
        value = value.strip()

        if not re.match(pattern, value):
            message = f"Value does not satisfy the rule {pattern}"
            raise typer.BadParameter(message, ctx=ctx, param=param)

        return value

    return factory


def user_profile_callback(
    ctx: typer.Context,
) -> None:
    """Inject required user_profile into context."""
    user_profile = get_user_profile(ctx.obj.config, ctx.obj.profile_name)
    ctx.obj.profile = user_profile


def extract_account(
    ctx: typer.Context,
    account: typing.Optional[str] = None,
) -> typing.Tuple[dict, typing.Optional[dict]]:
    """Set up account header and params."""
    profile_account = ctx.obj.get_account()
    if profile_account != "root" and account is not None:
        raise exit_with_output(
            msg="Only root account admins can impersonate other accounts.",
            exit_code=1,
        )

    headers = {"X-Account": profile_account}
    params = {"account": account} if account else None

    return headers, params
