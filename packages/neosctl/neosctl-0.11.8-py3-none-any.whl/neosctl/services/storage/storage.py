import pathlib
import typing

import minio
import typer
from minio.commonconfig import CopySource

from neosctl import util

app = typer.Typer()

bucket_app = typer.Typer()
object_app = typer.Typer()
tagging_app = typer.Typer()

BUCKET_NAME_PATTERN = "^[a-z0-9][a-z0-9\\.\\-]{2,62}$"
OBJECT_NAME_PATTERN = "^[a-zA-Z0-9!\\ \\.\\-\\_*\\'\\(\\)]{1,255}$"

BUCKET_NAME_ARGUMENT = typer.Argument(
    ...,
    help="Bucket name",
    callback=util.validate_regex(BUCKET_NAME_PATTERN),
)

# Don't use regex as OBJECT_NAME can be `path/to/my/file.txt` etc. which could easily exceed 255 and break allowed chars
# minio just checks that object_name is not empty.
OBJECT_NAME_ARGUMENT = typer.Argument(
    ...,
    help="Object name",
    callback=util.validate_string_not_empty,
)

app.add_typer(bucket_app, name="bucket", help="Manage object buckets.")
app.add_typer(object_app, name="object", help="Manage objects.")
object_app.add_typer(tagging_app, name="tags", help="Manage object tags.")


def _generate_client(ctx: typer.Context) -> minio.Minio:
    credential = util.get_user_credential(ctx.obj.credential, ctx.obj.profile_name)
    secure = ctx.obj.storage_api_url.startswith("https://")
    host = ctx.obj.storage_api_url.rstrip("/").replace("https://", "").replace("http://", "")

    return minio.Minio(  # nosec: B106
        host,
        access_key=credential.access_key_id,
        secret_key=credential.secret_access_key,
        secure=secure,
    )


@bucket_app.command(name="create")
def create_bucket(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
) -> None:
    """Create new bucket."""
    client = _generate_client(ctx)

    print(client.make_bucket(bucket_name))


@bucket_app.command(name="list")
def list_buckets(
    ctx: typer.Context,
) -> None:
    """List buckets."""
    client = _generate_client(ctx)

    print([str(x) for x in client.list_buckets()])


@bucket_app.command(name="delete")
def delete_bucket(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
) -> None:
    """Delete bucket."""
    client = _generate_client(ctx)
    print(client.remove_bucket(bucket_name))


@object_app.command(name="create")
def create_object(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    object_name: str = OBJECT_NAME_ARGUMENT,
    file: str = typer.Argument(
        ...,
        help="Path to the object file.",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Create object."""
    client = _generate_client(ctx)
    client.fput_object(
        bucket_name,
        object_name,
        file,
    )
    print(f"Object {object_name} is added to the bucket {bucket_name}")


@object_app.command(name="list")
def list_objects(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    prefix: typing.Union[str, None] = typer.Option(None, help="Path prefix"),
    *,
    recursive: bool = typer.Option(False, help="Recursively list bucket contents"),
) -> None:
    """List objects."""
    client = _generate_client(ctx)
    print(
        [
            obj._object_name  # noqa: SLF001
            for obj in client.list_objects(bucket_name, prefix=prefix, recursive=recursive)
        ],
    )


@object_app.command(name="copy")
def copy_object(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    prefix: typing.Union[str, None] = typer.Option(None, help="Path prefix"),
    target_bucket_name: str = BUCKET_NAME_ARGUMENT,
    target_prefix: typing.Union[str, None] = typer.Option(None, help="Target path prefix"),
) -> None:
    """List objects."""
    client = _generate_client(ctx)
    for obj in client.list_objects(bucket_name, prefix=prefix, recursive=True):
        if prefix is None and target_prefix is not None:
            # No prefix, prepend target prefix onto path `/path/to/file` -> `/target/path/to/file`
            target_object = f"{target_prefix.rstrip('/')}/{obj._object_name}"  # noqa: SLF001
        elif prefix is not None and target_prefix is not None:
            # Have prefix and target_prefix, replace prefix with target prefix `/prefix/file` -> `/target/file`
            target_object = obj._object_name.replace(prefix.rstrip("/"), target_prefix.rstrip("/"))  # noqa: SLF001
        else:
            # Have prefix and no target, or no prefix and no target `/path/to/file` -> `/path/to/file`
            target_object = obj._object_name  # noqa: SLF001

        client.copy_object(
            target_bucket_name,
            target_object,
            CopySource(
                bucket_name,
                obj._object_name,  # noqa: SLF001
            ),
        )


@object_app.command(name="get")
def get_object(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    object_name: str = OBJECT_NAME_ARGUMENT,
    file: str = typer.Argument(
        ...,
        help="Path to file where to store the object.",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Get object."""
    client = _generate_client(ctx)

    response = client.get_object(bucket_name, object_name)

    with pathlib.Path(file).open("wb") as fh:
        fh.write(response.data)


@object_app.command(name="delete")
def delete_object(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    object_name: str = OBJECT_NAME_ARGUMENT,
) -> None:
    """Delete object."""
    client = _generate_client(ctx)

    client.remove_object(bucket_name, object_name)
    print(f"Object {object_name} is deleted from the bucket {bucket_name}.")  # type: ignore[reportGeneralTypeIssues] # noqa: E501


@tagging_app.command(name="set")
def set_object_tags(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    object_name: str = OBJECT_NAME_ARGUMENT,
    tags: typing.List[str] = typer.Argument(
        ...,
        help="Tags as pairs of key=value",
        callback=util.validate_strings_are_not_empty,
    ),
) -> None:
    """Set object tags. Be aware that this command overwrites any tags that are already set to the object."""
    client = _generate_client(ctx)

    minio_tags = minio.commonconfig.Tags.new_object_tags()  # type: ignore[reportGeneralTypeIssues]
    for tag in tags:
        key, value = tag.split("=", 1)
        minio_tags[key] = value
    client.set_object_tags(bucket_name, object_name, minio_tags)


@tagging_app.command(name="get")
def get_object_tags(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    object_name: str = OBJECT_NAME_ARGUMENT,
) -> None:
    """Get object tags."""
    client = _generate_client(ctx)

    print(client.get_object_tags(bucket_name, object_name))


@tagging_app.command(name="delete")
def delete_object_tags(
    ctx: typer.Context,
    bucket_name: str = BUCKET_NAME_ARGUMENT,
    object_name: str = OBJECT_NAME_ARGUMENT,
) -> None:
    """Delete object tags."""
    client = _generate_client(ctx)

    print(client.delete_object_tags(bucket_name, object_name))
