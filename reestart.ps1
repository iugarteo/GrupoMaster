docker-compose -f private/rabbit/rabbit/docker-compose.yml up -d 
docker-compose -f haproxy/docker-compose.yml up -d 
docker-compose -f private/TodoLoDemas/docker-compose.yml up -d 