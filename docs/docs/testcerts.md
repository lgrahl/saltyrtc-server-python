# Test Certificates

To be able to start the SaltyRTC server, you need to specify a TLS key and
certificate. In production you will want to use a certificate signed by a
trusted CA, but for testing purposes, the easiest way is to create a
self-signed certificate.

## Generating a Test Certificate

Use the following command to create such a certificate, valid for `localhost`
during the next 90 days:

    $ openssl req \
           -newkey rsa:3072 \
           -x509 \
           -nodes \
           -keyout saltyrtc.key \
           -new \
           -out saltyrtc.crt \
           -subj /CN=localhost \
           -reqexts SAN \
           -extensions SAN \
           -config <(cat /etc/ssl/openssl.cnf \
             <(printf '[SAN]\nsubjectAltName=DNS:localhost')) \
           -sha256 \
           -days 90

## Importing

### Chrome / Chromium

The best way to import this certificate into Chrome is via the command line:

    $ certutil -d sql:$HOME/.pki/nssdb \
        -A -t "P,," -n saltyrtc-test-ca \
        -i saltyrtc.crt

Then make sure to restart your browser (or simply visit `chrome://restart`).

### Firefox

In Firefox the easiest way to add your certificate to the browser is to start
the SaltyRTC server (e.g. on `localhost` port 8765), then to visit the
corresponding URL via https (e.g. `https://localhost:8765`). Then, in the
certificate warning dialog that pops up, choose "Advanced" and add a permanent
exception.
