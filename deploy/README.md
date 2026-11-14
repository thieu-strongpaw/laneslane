# Deploy on strongpawkeep: Apache + mod_wsgi + Cloudflare Tunnel

The existing `strongpawcoding` site stays on port 80. This app uses its own Apache daemon process, virtual environment, data directory, and loopback listener on port 8080. No Gunicorn or Nginx is needed. cloudflared already runs on this server; reuse its tunnel.

## 1. Prepare the server

These commands target your Debian/Ubuntu-style Apache installation. Use system Python 3.12 (`/usr/bin/python3`) to create the environment. mod_wsgi must be compiled for the same base Python installation/version; confirm the existing module's Python version in Apache startup logs or package information before enabling this site. Do not replace the server's global WSGI module or reuse the other site's virtual environment.

```bash
sudo apt install git python3-venv
sudo useradd --system --user-group --home-dir /var/lib/laneslane --shell /usr/sbin/nologin laneslane
sudo install -d -o laneslane -g www-data -m 2750 /srv/laneslane /var/lib/laneslane /var/lib/laneslane/media /srv/laneslane/staticfiles
sudo install -d -o root -g laneslane -m 0750 /etc/laneslane
sudo git clone https://github.com/thieu-strongpaw/laneslane.git /srv/laneslane/app
sudo chown -R laneslane:www-data /srv/laneslane/app
cd /srv/laneslane/app
sudo -u laneslane /usr/bin/python3 -m venv .venv
sudo -u laneslane .venv/bin/pip install -r requirements.txt
sudo install -o root -g laneslane -m 0640 deploy/production.env.example /etc/laneslane/production.env
```

Edit `/etc/laneslane/production.env` as root. Replace the example domain and secret. Generate a secret using `python3 -c 'import secrets; print(secrets.token_urlsafe(64))'`. Keep the actual file off Git. Entries use `NAME=value`, one per line; quote values containing spaces. Do not use shell substitutions or `export`. Production settings read this file directly for both Apache and management commands. SMTP entries are optional unless outgoing email is needed.

The new site needs a commit containing these deployment files; the original beta tag does not include them. After pushing from your laptop, check out that commit or a new release tag on the server.

## 2. Initialize the website

To retain your laptop content, stop writes on the laptop and copy its `db.sqlite3` plus the complete `media/` directory into `/var/lib/laneslane/`. Otherwise migrations create an empty database. Set copied files' ownership to `laneslane:www-data`, with group-readable files and group-traversable directories so Apache can read artwork. The database directory must be writable by laneslane.

```bash
cd /srv/laneslane/app
sudo -u laneslane .venv/bin/python manage.py migrate --settings=laneslane.production
sudo -u laneslane .venv/bin/python manage.py collectstatic --noinput --settings=laneslane.production
sudo -u laneslane .venv/bin/python manage.py check --deploy --settings=laneslane.production
sudo -u laneslane .venv/bin/python manage.py createsuperuser --settings=laneslane.production
```

Skip createsuperuser if you copied an existing admin account. The deployment check retains two deliberate HSTS warnings: include-subdomains and browser preload are disabled so this app does not impose HTTPS policy on your other services.

## 3. Enable the Apache site

Replace `art.example.com` in `deploy/apache.conf` with your real public hostname. Port 8080 was free in the supplied server output; check again before enabling. If changing it, change both the Listen and VirtualHost lines and the tunnel route. Do not add a duplicate Listen directive if you already configured this port elsewhere.

```bash
sudo a2enmod headers
sudo cp deploy/apache.conf /etc/apache2/sites-available/laneslane.conf
sudo a2ensite laneslane
sudo apache2ctl configtest
```

Only if configtest reports `Syntax OK`:

```bash
sudo systemctl reload apache2
curl -I -H 'Host: art.example.com' http://127.0.0.1:8080/
```

Expect HTTP 200. Diagnose errors with `/var/log/apache2/laneslane-error.log`. Keep your existing `strongpawcoding.conf` unchanged. The existing global ServerName warning is informational and does not prevent this setup.

## 4. Cloudflare portal

Open your existing tunnel and add a published application route for the chosen hostname with HTTP service `127.0.0.1:8080`. Keep the existing site's route. Enable Cloudflare's Always Use HTTPS for visitor requests. Apache's dedicated loopback listener asserts HTTPS to Django, so it must remain restricted to this trusted HTTPS tunnel path. No router port forwarding is required. If your tunnel config overrides the HTTP Host header, set it to your public hostname.

Test the homepage `/`, gallery images, contact page, admin login, saving changes and artwork uploads through the public HTTPS domain. `/MainPage/` redirects to `/`. Reboot and verify Apache and cloudflared return automatically.

## 5. Updates and backups

Develop and test on the laptop, then commit and push. On the server, take a consistent backup of the live database and media before migrations. You can disable only this virtual host during maintenance (`sudo a2dissite laneslane` then reload Apache), leaving the other site running. Fetch and check out the desired commit/tag as the laneslane user, install requirements, migrate and collectstatic using the commands above. Re-enable with `sudo a2ensite laneslane`, run configtest, and reload Apache. For ordinary code/config-file updates without migrations, `sudo touch /srv/laneslane/app/deploy/apache.wsgi` recycles only this site's daemon processes on the next request.

Store backups outside this PC. Live content belongs in `/var/lib/laneslane`, outside the code checkout; do not overwrite it with older laptop copies. A code rollback after schema changes can require restoring the matching database backup. Pushing to GitHub does not automatically update the server.
