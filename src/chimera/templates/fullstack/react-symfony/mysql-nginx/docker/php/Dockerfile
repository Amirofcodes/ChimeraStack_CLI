# docker/php/Dockerfile

FROM php:8.3-fpm-alpine AS app

# Install system dependencies
RUN apk add --no-cache \
    acl \
    fcgi \
    file \
    gettext \
    git \
    gnu-libiconv \
    bash \
    icu-dev \
    libzip-dev \
    nodejs \
    npm

# Install PHP extensions
RUN set -eux; \
    docker-php-ext-configure zip; \
    docker-php-ext-install -j$(nproc) \
    intl \
    zip \
    pdo_mysql \
    ; \
    pecl install \
    apcu \
    xdebug \
    ; \
    pecl clear-cache; \
    docker-php-ext-enable \
    apcu \
    opcache \
    ;

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Install Symfony CLI
RUN curl -1sLf 'https://dl.cloudsmith.io/public/symfony/stable/setup.alpine.sh' | bash \
    && apk add symfony-cli

WORKDIR /var/www/html

# Copy PHP configurations
COPY ../docker/php/php.ini /usr/local/etc/php/conf.d/
COPY ../docker/php/www.conf /usr/local/etc/php-fpm.d/

# Development stage
FROM app AS app_dev

ENV APP_ENV=dev
RUN docker-php-ext-enable xdebug

# Production stage
FROM app AS app_prod

ENV APP_ENV=prod

# Copy application files
COPY . .
RUN set -eux; \
    mkdir -p var/cache var/log; \
    composer install --prefer-dist --no-dev --no-progress --no-scripts --no-interaction; \
    composer dump-autoload --classmap-authoritative --no-dev; \
    composer symfony:dump-env prod; \
    composer run-script --no-dev post-install-cmd; \
    chmod +x bin/console; sync; \
    chown -R www-data:www-data var