#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
[[ $(id -u) == 0 ]] || { echo 'Please run as root.' >&2; exit 1; }
[[ -f dist/index.html && -f dist/source/index.json.gz ]] || { echo 'Full data build is missing.' >&2; exit 1; }
port=${PORT:-80}
[[ $port =~ ^[0-9]+$ ]] && ((port>0 && port<65536)) || exit 1
if command -v ss >/dev/null && ss -ltnp "sport = :$port" | tail -n +2 | grep -q .; then
  ss -ltnp "sport = :$port" | grep -q nginx || { echo "Port $port is occupied. Run PORT=8080 bash install.sh instead." >&2; exit 1; }
fi
if ! command -v nginx >/dev/null; then
  if command -v apt-get >/dev/null; then apt-get update; apt-get install -y nginx;
  elif command -v dnf >/dev/null; then dnf install -y nginx;
  elif command -v yum >/dev/null; then yum install -y nginx;
  else echo 'Install nginx with your operating system package manager first.' >&2; exit 1; fi
fi
base=/var/www/inception-microscope
release="$base/releases/$(date +%Y%m%d-%H%M%S)-$$"
config=/etc/nginx/conf.d/inception-microscope.conf
mkdir -p "$release" /etc/nginx/conf.d
cp -R dist/. "$release/"
find "$release" -type d -exec chmod 755 {} +
find "$release" -type f -exec chmod 644 {} +
previous=$(readlink "$base/current" || true)
backup="$config.backup.$(date +%Y%m%d-%H%M%S)"
[[ ! -f $config ]] || cp -p "$config" "$backup"
rollback() {
  if [[ -f $backup ]]; then cp -p "$backup" "$config"; else rm -f "$config"; fi
  if [[ -n $previous ]]; then ln -sfn "$previous" "$base/current"; else rm -f "$base/current"; fi
}
trap 'rollback' ERR
ln -sfn "$release" "$base/current"
cat > "$config" <<EOF
server {
    listen $port;
    server_name 47.100.101.127;
    root $base/current;
    index index.html;
    autoindex off;
    sendfile on;
    tcp_nopush on;
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/css application/javascript application/json image/svg+xml;
    location = /index.html { add_header Cache-Control "no-cache"; }
    location ~ \\.(js|css)$ { add_header Cache-Control "no-cache"; }
    location ~ \\.(avif|png|jpg|jpeg|bin|gz)$ {
        # .gz is explicitly decompressed by app.js: do not add Content-Encoding.
        add_header Cache-Control "public, max-age=86400";
        try_files \$uri =404;
    }
    location ~ /\\. { deny all; }
    location / { try_files \$uri \$uri/ =404; }
}
EOF
nginx -t
if command -v restorecon >/dev/null; then restorecon -R "$base" || true; fi
if command -v systemctl >/dev/null; then
  systemctl enable nginx
  if systemctl is-active --quiet nginx; then systemctl reload nginx; else systemctl start nginx; fi
else nginx -s reload || nginx; fi
trap - ERR
echo "Installed: http://47.100.101.127:$port/#level=1"
echo 'If external access fails, check the cloud security group and local firewall for this port.'
echo "Previous release: ${previous:-none}; current: $release"
