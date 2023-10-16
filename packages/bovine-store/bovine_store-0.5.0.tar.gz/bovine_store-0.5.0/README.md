# bovine_store

`bovine_store` is meant to be the module handling storing of
local ActivityPub objects and caching of remote ActivityPub
objects.

## Usage

bovine_store assumes that a database connection is initialized using [tortoise-orm](https://tortoise.github.io/). See `examples/basic_app.py` for how to do this in the context of a quart app.

## TODO

- [ ] When properties of actor are updated, send an update Activity
  - Doesn't fit into the current bovine framework ... bovine_store doesn't know how to send activities
- [ ] Generally rework the actor properties mechanism. It is currently not possible to emulate say Mastodon featured collection with it.
- [ ] bovine_store.models.BovineActorKeyPair needs renamings; and work, e.g. a future identity column should have a uniqueness constraint.
- [ ] Generally the code quality is not as high as it should be.

## Examples

A demonstration webserver can be seen using

```bash
poetry run python examples/basic_app.py
```

Note this is a very basic example. Instructions what the example does are
printed to the command line after start.

Note: This example creates two files `db.sqlite3`, which contains the
database and `context_cache.sqlite`, which contains the cache of json-ld
contexts.

## Running tests

For sqlite3

```bash
poetry run pytest
```

For postgres

```bash
BOVINE_DB_URL=postgres://postgres:secret@postgres:5432/postgres poetry run pytest
```
