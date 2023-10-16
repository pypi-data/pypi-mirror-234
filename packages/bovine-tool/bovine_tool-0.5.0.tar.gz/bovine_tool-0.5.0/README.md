# bovine_tool

bovine_tool provides a CLI interface to manage bovine.

## Configuration

The default database connection is "sqlite://bovine.sqlite3". This can be overwridden with the environment variable "BOVINE_DB_URL".

## Quick start

To register a new user with a FediVerse handle use

```bash
python -m bovine_tool.register fediverse_handle [--domain DOMAIN]
```

the domain must be specified. This creates the account `acct:fediverse_handle@DOMAIN`.

## Managing users

```bash
python -m bovine_tool.manage bovine_name
```

displays the user.

To add a did key for [the Moo Client Registration Flow](https://blog.mymath.rocks/2023-03-25/BIN2_Moo_Client_Registration_Flow) with a BovineClient use

```bash
python -m bovine_tool.manage bovine_name --did_key key_name did_key
```

Furthermore, using `--properties` the properties can be over written.

## Cleaning the database

```bash
python -m bovine_tool.cleanup
```

to delete all remote objects older than 3 days. This should be expanded to make the variables configurable and delete a bunch of other stuff, e.g.

- remove inbox, outbox entries older than 14 days
- have a "timeline" of outbox entries to display on a public profile
- remove all local entries not in inbox, outbox, or timeline
- remove deleted items older than 1 month
- make time frames configurable
