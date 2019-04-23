#!/bin/sh

docker run -it --rm \
    -p 4000:4000 \
    -p 4001:4001 \
    -p 4002:4002 \
    -v $PWD:/usr/src/game \
    --user $UID:$GID \
    evennia/evennia:develop

# 4000: Telnet
# 4001: Webserver
# 4002: Websocket
