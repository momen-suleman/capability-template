# Template container for an Orqen external capability.
#
# This is the unit of isolation: Orqen's engine never runs your code
# in-process -- it only ever sends one bounded HTTP POST to whatever
# container you expose here. Build on this however your wrapped repo
# needs to (different base image, extra deps, a compiled binary instead
# of Python) as long as the container answers the same contract.
FROM python:3.12-slim

WORKDIR /app
COPY server.py .

ENV PORT=9321
EXPOSE 9321

CMD ["python", "server.py"]
