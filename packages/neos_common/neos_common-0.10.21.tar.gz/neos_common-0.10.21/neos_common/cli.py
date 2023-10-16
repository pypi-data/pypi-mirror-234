"""Common utils to support neos cli applications."""
import typing

from yoyo import get_backend, read_migrations
from yoyo.migrations import topological_sort


def migration_upgrade(postgres_dsn: str) -> None:
    backend = get_backend(postgres_dsn)

    migrations = read_migrations("migrations")

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))


def migration_downgrade(postgres_dsn: str, count: typing.Union[int, None] = 1) -> None:
    backend = get_backend(postgres_dsn)

    migrations = backend.to_rollback(
        read_migrations("migrations"),
    )
    if count:
        migrations = migrations[:count]

    with backend.lock():
        # Rollback selected migrations (default is latest)
        backend.rollback_migrations(migrations, force=True)


def migration_history(postgres_dsn: str) -> typing.Generator[typing.Tuple[str, str], None, None]:
    backend = get_backend(postgres_dsn)
    migrations = read_migrations("migrations")

    with backend.lock():
        migrations = migrations.__class__(topological_sort(migrations))
        applied = backend.to_rollback(migrations)

    return (("A" if m in applied else " ", m.id) for m in migrations)
