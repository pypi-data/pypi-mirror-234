# bovine_herd

`bovine_herd` is a `bovine` powered ActivityPub server, which interoperates with the rest of the FediVerse.

Running:

```bash
pip install bovine_herd
hypercorn bovine_herd:app
```

This will start `bovine_herd` using an sqlite3 database.

## Interacting with the fediverse

Assume that you alias `$DOMAIN` so that it redirects to the above server. Then by running

```bash
pip install bovine_tool
python -mbovine_tool.register --domain $DOMAIN moocow
```

you create a new account for __moocow__. This command returns its bovine name, which will be of the form `moocow + uuid4()`, e.g. `moocow_09c80006-483c-4826-b48c-cf5134b4e898`. By running:

```bash
python -mbovine_tool.manage --new_did_key $BOVINE_NAME
```

you will be given a secret (an Ed25519 private key, i.e. starts with `z3u2`). Once you have this secret, you can send a message via

```bash
python -mbovine.msg --secret $SECRET --host $DOMAIN moooo
```

## Configuration

The default database connection is "sqlite://bovine.sqlite3". This can be overwridden with the environment variable "BOVINE_DB_URL".

- `BOVINE_REDIS` represents how to reach redis, e.g. `redis://localhost`. If not set, redis is not used. Redis is necessary when using more than one worker.
