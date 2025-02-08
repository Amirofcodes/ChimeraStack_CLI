# nginx/docker-healthcheck.sh 
#!/bin/sh
set -e

nginx -t || exit 1

if [ $(wget -q -O - http://localhost/health | grep -c "healthy") -eq 0 ]; then
    exit 1
fi

exit 0