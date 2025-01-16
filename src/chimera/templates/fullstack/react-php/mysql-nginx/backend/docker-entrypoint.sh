#!/bin/sh
set -e

# Create required directories and set permissions
mkdir -p /var/log/nginx
mkdir -p /var/log/php
touch /var/log/php/fpm-error.log
chown -R www-data:www-data /var/log/nginx
chown -R www-data:www-data /var/log/php
chmod 755 /var/log/nginx
chmod 755 /var/log/php

# Start PHP-FPM
php-fpm -D

# Wait a moment for PHP-FPM to be ready
sleep 2

# Start Nginx in foreground
nginx -g "daemon off;"
