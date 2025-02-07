#!/bin/sh
set -e

if [ $(php-fpm -t 2>&1 | grep -c "configuration file test is successful") -eq 0 ]; then
    exit 1
fi

exit 0

# docker/nginx/docker-healthcheck.sh
#!/bin/sh
set -e

nginx -t || exit 1

if [ $(wget -q -O - http://localhost/health | grep -c "healthy") -eq 0 ]; then
    exit 1
fi

exit 0