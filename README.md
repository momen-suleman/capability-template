# capability-template

Starting point for wrapping any tool as an
[Orqen Mission Studio](https://github.com/momen-suleman/Orqen) external
capability. Fork this, replace the logic in `handle(text)` inside
`server.py`, and you have a working capability container.

## Contract

Whatever runs behind the endpoint must answer:

```
POST /   { "input": "<text>" }   ->   { "result": "<text>" }
GET  /   (any response = reachable, used by Orqen's "Test connection")
```

Orqen's engine only ever makes one bounded HTTP POST here — it never builds,
downloads, or inspects your code directly.

## Run it

```bash
docker build -t my-capability .
docker run -p 9321:9321 my-capability
```

## Using it in Orqen

Open **Capabilities → New capability** in Orqen Mission Studio and set the
Endpoint to `http://127.0.0.1:9321` (or wherever you've deployed it). Once
it's working, consider submitting it to the
[community registry](https://github.com/momen-suleman/orqen-registry) via
Orqen's **Publish a package** dialog.
