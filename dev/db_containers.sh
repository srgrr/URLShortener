#!/bin/bash
set -x

# Redis params
redis_port=$1
redis_insight_port=$2
redis_container_name=redis-stack-${redis_port}-${redis_insight_port}

# Stop the previous containers
docker stop ${redis_container_name}

# Reset the docker system
docker rm ${redis_container_name}

# Leave if we we are only stopping stuff here
stop_rm_only=$3
if [ $stop_rm_only == "true" ]; then
  exit 0
fi


# Redis
docker run \
-d --name ${redis_container_name} \
-p ${redis_port}:${redis_port} \
-p ${redis_insight_port}:${redis_insight_port} \
redis/redis-stack:latest
