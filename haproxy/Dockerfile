FROM haproxy:1.7
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY certs/frontend/server.pem /usr/local/etc/haproxy/server.pem
RUN chmod 777 /usr/local/etc/haproxy/server.pem