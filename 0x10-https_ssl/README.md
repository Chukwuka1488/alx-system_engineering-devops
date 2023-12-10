### HTTPS SSL

**************** 2 **************
The configuration snippet you've provided is for HAProxy, a high-performance TCP/HTTP load balancer. Here's an explanation of the key parts of the configuration:

**Global Section**:
- `log /dev/log local0` and `log /dev/log local1 notice`: These lines configure logging. The first line logs general messages, and the second logs only 'notice' level messages.
- `chroot /var/lib/haproxy`: This line changes the root directory to `/var/lib/haproxy` for security purposes, limiting the files HAProxy can access.
- `stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners`: This creates a UNIX socket for accessing HAProxy statistics.
- `stats timeout 30s`: Sets a timeout for the stats socket.
- `user haproxy` and `group haproxy`: These lines set the user and group that HAProxy will run as.
- `daemon`: Runs HAProxy as a daemon.

**SSL Configuration**:
- `ca-base /etc/ssl/certs` and `crt-base /etc/ssl/private`: These lines set the default locations for SSL certificate authorities and certificates.
- `ssl-default-bind-ciphers` and `ssl-default-bind-ciphersuites`: These lines configure the default ciphers and cipher suites for SSL connections.
- `ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets`: Sets the minimum version of TLS to accept and disables TLS tickets.

**Defaults Section**:
- `log global`: Uses the global logging configuration.
- `mode http`: Sets the mode to HTTP.
- `option httplog`: Enables HTTP-specific logging.
- `option dontlognull`: Do not log null connections.
- `timeout connect`, `timeout client`, and `timeout server`: Set various timeouts.
- `errorfile`: Specifies custom error files for different HTTP error codes.

**Frontend clickviral-frontend**:
- `bind *:80`: Listens on all interfaces on port 80 (HTTP).
- `http-request redirect scheme https code 301 unless { ssl_fc }`: Redirects HTTP requests to HTTPS unless the connection is already SSL.
- `http-request set-header X_Forwarded-Proto http`: Sets the X_Forwarded-Proto header to HTTP.
- `default_backend clickviral-backend`: Sets the default backend to `clickviral-backend`.

**Frontend clickviral-frontend-https**:
- `bind *:443 ssl crt /etc/haproxy/certs/clickviral.tech.pem`: Listens on all interfaces on port 443 (HTTPS) and specifies the SSL certificate to use.
- `http-request set-header X-Forwarded-Proto https`: Sets the X_Forwarded-Proto header to HTTPS.
- `default_backend clickviral-backend`: Sets the default backend to `clickviral-backend`.

**Backend clickviral-backend**:
- `balance roundrobin`: Uses round-robin load balancing.
- `server 151666-web-01 100.25.190.21:80 check`: Defines a server in the backend with its IP and port, with health checks enabled.
- `server 151666-web-02 54.160.77.90:80 check`: Another server definition in the backend.

This configuration sets up HAProxy to handle both HTTP and HTTPS traffic, redirecting HTTP to HTTPS, and load balancing between two backend servers. It also includes SSL termination for secure connections.