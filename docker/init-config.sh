#!/bin/bash
docker exec -it configsvr mongosh --port 27019 --eval '
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "configsvr:27019" }]
})
'
