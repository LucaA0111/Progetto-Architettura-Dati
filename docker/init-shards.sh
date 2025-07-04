#!/bin/bash

for i in 1 2 3 4; do
  docker exec -it shard$i mongosh --port $((27019 - i)) --eval "
rs.initiate({
  _id: \"shard${i}ReplSet\",
  members: [{ _id: 0, host: \"shard${i}:$((27019 - i))\" }]
})
"
done
