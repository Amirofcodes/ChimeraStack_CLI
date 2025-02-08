# php/docker-healthcheck.sh
#!/bin/sh
set -e

if [ $(php-fpm -t 2>&1 | grep -c "configuration file test is successful") -eq 0 ]; then
    exit 1
fi

exit 0