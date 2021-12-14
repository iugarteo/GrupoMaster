FROM haproxy:latest
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY certs/backend/haproxy.pem /usr/local/etc/haproxy/haproxy.pem
COPY certs/frontend/server.pem /usr/local/etc/haproxy/server.pem
#RUN chmod 777 /usr/local/etc/haproxy/server.pem
#RUN chmod 777 /usr/local/etc/haproxy/haproxy.pem