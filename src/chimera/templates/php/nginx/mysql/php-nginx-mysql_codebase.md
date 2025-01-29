# config/development.yaml

```yaml
project:
  name: ${PROJECT_NAME}
  language: php
  framework: none
  environment: development

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - ${MYSQL_PORT}:3306
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - ${NGINX_PORT}:80
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
    depends_on:
      - php
    networks:
      - app_network
    healthcheck:
      test:
        [
          "CMD",
          "wget",
          "--quiet",
          "--tries=1",
          "--spider",
          "http://localhost/ping",
        ]
      interval: 10s
      timeout: 5s
      retries: 3

  php:
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    environment:
      PHP_DISPLAY_ERRORS: ${PHP_DISPLAY_ERRORS}
      PHP_ERROR_REPORTING: ${PHP_ERROR_REPORTING}
      PHP_MEMORY_LIMIT: ${PHP_MEMORY_LIMIT}
      PHP_MAX_EXECUTION_TIME: ${PHP_MAX_EXECUTION_TIME}
      PHP_POST_MAX_SIZE: ${PHP_POST_MAX_SIZE}
      PHP_UPLOAD_MAX_FILESIZE: ${PHP_UPLOAD_MAX_FILESIZE}
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "php-fpm", "-t"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  mysql_data:
    driver: local
    name: ${PROJECT_NAME}_mysql_data
  php_logs:
    driver: local
    name: ${PROJECT_NAME}_php_logs

networks:
  app_network:
    driver: bridge
    name: ${PROJECT_NAME}_network

```

# docker-compose.yml

```yml
services:
  mysql:
    image: mysql:8.0
    container_name: ${PROJECT_NAME}-mysql
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - "${MYSQL_PORT}:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/mysql/my.cnf:/etc/mysql/conf.d/custom.cnf:cached
    networks:
      - app_network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: ${PROJECT_NAME}-phpmyadmin
    environment:
      PMA_HOST: mysql
      PMA_USER: ${DB_USERNAME}
      PMA_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${PHPMYADMIN_PORT}:80"
    networks:
      - app_network

  php:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
    container_name: ${PROJECT_NAME}-php
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    networks:
      - app_network

  nginx:
    image: nginx:alpine
    container_name: ${PROJECT_NAME}-nginx
    ports:
      - "${NGINX_PORT}:80"
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:cached
    depends_on:
      - php
    networks:
      - app_network

networks:
  app_network:
    name: ${PROJECT_NAME}_network

volumes:
  mysql_data:
    name: ${PROJECT_NAME}_mysql_data
  php_logs:
    name: ${PROJECT_NAME}_php_logs

```

# docker/mysql/my.cnf

```cnf
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
default_authentication_plugin = mysql_native_password

max_connections = 100
thread_cache_size = 8
thread_stack = 256K

innodb_buffer_pool_size = 256M
innodb_buffer_pool_instances = 4
innodb_log_file_size = 64M
innodb_flush_method = O_DIRECT
innodb_flush_log_at_trx_commit = 2
innodb_file_per_table = 1
innodb_strict_mode = 1

tmp_table_size = 32M
max_heap_table_size = 32M

max_allowed_packet = 64M
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4

```

# docker/nginx/conf.d/default.conf

```conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html/public;
    index index.php index.html;

    location = /health {
        access_log off;
        add_header Content-Type text/plain;
        return 200 'healthy';
    }

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_buffer_size 32k;
        fastcgi_buffers 16 16k;
        fastcgi_read_timeout 300;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires max;
        access_log off;
        add_header Cache-Control "public";
    }
}

```

# docker/php/Dockerfile

```
FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    libpng-dev \
    libonig-dev \
    libzip-dev \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install \
    pdo \
    pdo_mysql \
    mbstring \
    zip \
    exif \
    gd

COPY docker/php/php.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker/php/www.conf /usr/local/etc/php-fpm.d/www.conf

RUN mkdir -p /var/log/php-fpm \
    && chown -R www-data:www-data /var/log/php-fpm

WORKDIR /var/www/html

USER www-data

```

# docker/php/php.ini

```ini
[PHP]
display_errors = ${PHP_DISPLAY_ERRORS}
display_startup_errors = ${PHP_DISPLAY_ERRORS}
error_reporting = ${PHP_ERROR_REPORTING}
log_errors = On
error_log = /var/log/php-fpm/php_errors.log
log_errors_max_len = 1024
ignore_repeated_errors = Off
ignore_repeated_source = Off
report_memleaks = On

memory_limit = ${PHP_MEMORY_LIMIT}
max_execution_time = ${PHP_MAX_EXECUTION_TIME}
post_max_size = ${PHP_POST_MAX_SIZE}
upload_max_filesize = ${PHP_UPLOAD_MAX_FILESIZE}
max_file_uploads = 20

[Date]
date.timezone = UTC

[Session]
session.save_handler = files
session.save_path = /tmp
session.gc_maxlifetime = 1800
session.gc_probability = 1
session.gc_divisor = 100

[opcache]
opcache.enable = 1
opcache.memory_consumption = 128
opcache.interned_strings_buffer = 8
opcache.max_accelerated_files = 4000
opcache.validate_timestamps = 1
opcache.revalidate_freq = 0
opcache.fast_shutdown = 1

[mysqlnd]
mysqlnd.collect_statistics = On
mysqlnd.collect_memory_statistics = On

```

# docker/php/www.conf

```conf
[global]
error_log = /var/log/php-fpm/error.log
log_level = notice

[www]
user = www-data
group = www-data

listen = 9000
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

pm = dynamic
pm.max_children = 10
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
pm.max_requests = 500

catch_workers_output = yes
decorate_workers_output = yes

php_admin_value[error_log] = /var/log/php-fpm/www-error.log
php_admin_flag[log_errors] = on

security.limit_extensions = .php

```

# public/index.php

```php
<?php
declare(strict_types=1);

require_once __DIR__ . '/../src/bootstrap.php';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($uri) {
    case '/':
        require __DIR__ . '/../src/pages/home.php';
        break;
    case '/info':
        phpinfo();
        break;
    case '/health':
        header('Content-Type: text/plain');
        echo 'healthy';
        break;
    default:
        http_response_code(404);
        echo "404 Not Found";
        break;
}

```

# src/bootstrap.php

```php
<?php
declare(strict_types=1);

error_reporting(E_ALL);
ini_set('display_errors', '1');

if (file_exists(__DIR__ . '/../.env')) {
    $env = parse_ini_file(__DIR__ . '/../.env');
    foreach ($env as $key => $value) {
        $_ENV[$key] = $value;
        putenv("$key=$value");
    }
}

spl_autoload_register(function ($class) {
    $file = __DIR__ . DIRECTORY_SEPARATOR . 
            str_replace(['\\', '/'], DIRECTORY_SEPARATOR, $class) . '.php';
    
    if (file_exists($file)) {
        require_once $file;
        return true;
    }
    return false;
});

$composerAutoloader = __DIR__ . '/../vendor/autoload.php';
if (file_exists($composerAutoloader)) {
    require_once $composerAutoloader;
}

```

# src/pages/home.php

```php
<?php

declare(strict_types=1);
$title = 'ChimeraStack PHP Development Environment';
$webPort = $_ENV['NGINX_PORT'] ?? '8080';
$dbPort = $_ENV['MYSQL_PORT'] ?? '3306';
$pmaPort = $_ENV['PHPMYADMIN_PORT'] ?? '8081';
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($title) ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
        }

        .status {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .info {
            background-color: #e2e3e5;
            border-color: #d6d8db;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        th,
        td {
            text-align: left;
            padding: 0.5rem;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>

<body>
    <h1><?= htmlspecialchars($title) ?></h1>

    <div class="card">
        <h2>Stack Overview</h2>
        <table>
            <tr>
                <th>Component</th>
                <th>Details</th>
                <th>Access</th>
            </tr>
            <tr>
                <td>Web Server</td>
                <td>Nginx + PHP-FPM</td>
                <td><a href="http://localhost:<?= $webPort ?>" target="_blank">localhost:<?= $webPort ?></a></td>
            </tr>
            <tr>
                <td>Database</td>
                <td>MySQL <?= $_ENV['DB_DATABASE'] ?></td>
                <td>localhost:<?= $dbPort ?></td>
            </tr>
            <tr>
                <td>Database GUI</td>
                <td>phpMyAdmin</td>
                <td><a href="http://localhost:<?= $pmaPort ?>" target="_blank">localhost:<?= $pmaPort ?></a></td>
            </tr>
        </table>
    </div>

    <div class="card info">
        <h2>Quick Links</h2>
        <ul>
            <li><a href="/info">PHP Info</a></li>
            <li><a href="http://localhost:<?= $pmaPort ?>" target="_blank">phpMyAdmin</a></li>
        </ul>
    </div>

    <div class="card">
        <h2>Database Connection Status</h2>
        <?php
        try {
            $dsn = "mysql:host={$_ENV['DB_HOST']};dbname={$_ENV['DB_DATABASE']}";
            $pdo = new PDO($dsn, $_ENV['DB_USERNAME'], $_ENV['DB_PASSWORD']);
            $version = $pdo->query('SELECT VERSION()')->fetchColumn();
            echo '<div class="status success">
                ✓ Connected to MySQL Server ' . htmlspecialchars($version) . '<br>
                Database: ' . htmlspecialchars($_ENV['DB_DATABASE']) . '<br>
                User: ' . htmlspecialchars($_ENV['DB_USERNAME']) . '
            </div>';
        } catch (PDOException $e) {
            echo '<div class="status error">✗ Database connection failed: ' . htmlspecialchars($e->getMessage()) . '</div>';
        }
        ?>
    </div>
</body>

</html>
```

# template.yaml

```yaml
name: "PHP/Nginx/MySQL Stack"
type: "PHP Development"
description: "PHP development environment with Nginx web server and MySQL database"
version: "1.0"
author: "ChimeraStack"

services:
  nginx:
    port_type: backend
    service_variant: php-nginx
    default_port: 8080
  phpmyadmin:
    port_type: admin
    service_variant: phpmyadmin
    default_port: 8081
  mysql:
    port_type: database
    service_variant: mysql
    default_port: 3306

env_template: ".env.example"
env_variables:
  PROJECT_NAME:
    description: "Project name"
    default: "${PROJECT_NAME}"
  DB_DATABASE:
    description: "Database name"
    default: "${PROJECT_NAME}"
  DB_USERNAME:
    description: "Database user"
    default: "${PROJECT_NAME}"
  DB_PASSWORD:
    description: "Database password"
    default: "secret"
  DB_ROOT_PASSWORD:
    description: "Database root password"
    default: "rootsecret"

network:
  name: "${PROJECT_NAME}_network"
  driver: bridge

```

