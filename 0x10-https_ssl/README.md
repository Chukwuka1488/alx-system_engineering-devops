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

Lines 10 to 17 in your HAProxy configuration file are specifying default settings for SSL/TLS encryption. These lines are crucial for setting up a secure environment for your HTTPS connections. Here's a breakdown of what each line means and where you can get the required information:

1. **`ca-base /etc/ssl/certs`**:
   - This line specifies the default folder where HAProxy looks for CA (Certificate Authority) certificates.
   - The `/etc/ssl/certs` directory is standard in many Linux distributions and typically contains trusted CA certificates.

2. **`crt-base /etc/ssl/private`**:
   - This sets the default directory where HAProxy looks for SSL/TLS certificates.
   - You should place your SSL/TLS certificates in the `/etc/ssl/private` directory, or change this path to the directory where you store your certificates.

3. **SSL Cipher and Cipher Suites**:
   - The next lines set the default ciphers and cipher suites for SSL/TLS connections. These determine the algorithms that will be used for encryption, decryption, and key exchange.
   - `ssl-default-bind-ciphers` and `ssl-default-bind-ciphersuites` are configured with a list of secure cipher suites. 
   - These specific values are generally recommended for a balance of security and compatibility, as suggested by the Mozilla SSL Configuration Generator.

4. **`ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets`**:
   - This line sets the minimum version of SSL/TLS protocol that HAProxy will accept (TLS version 1.2 in this case) and disables TLS tickets.
   - TLS 1.2 is recommended as a minimum because older versions (like SSLv3, TLS 1.0, and TLS 1.1) are considered less secure.

### How to Obtain SSL/TLS Certificates:

- If you don't have an SSL/TLS certificate for your domain (`gm-nig-ltd.tech`), you can obtain one from a Certificate Authority (CA). Let's Encrypt is a popular choice as it provides free certificates.
- Once you have your certificate, you should place the full chain and private key in a single file (e.g., `gm-nig-ltd.tech.pem`) and store it in the directory specified in your `crt-base` setting (or update the `bind` line in the `https-frontend` section to point to the correct location of your certificate file).

Remember, these settings are crucial for setting up secure HTTPS connections. Make sure the paths specified are correct and the certificate files are properly installed and have the correct permissions.