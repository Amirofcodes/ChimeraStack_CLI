FROM php:8.3-fpm-alpine AS app

# System dependencies
RUN apk add --no-cache \
    acl autoconf build-base linux-headers fcgi file gettext git \
    gnu-libiconv bash icu-dev libzip-dev nodejs npm $PHPIZE_DEPS

# PHP extensions
RUN docker-php-ext-configure zip \
    && docker-php-ext-install -j$(nproc) intl zip pdo_mysql \
    && pecl install apcu xdebug \
    && pecl clear-cache \
    && docker-php-ext-enable apcu opcache

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Create directories
WORKDIR /var/www/html
RUN mkdir -p var/cache var/log var/sessions /var/log/php \
    && chmod -R 777 var

# Copy configs
COPY php.ini /usr/local/etc/php/conf.d/
COPY www.conf /usr/local/etc/php-fpm.d/

# Copy application
COPY . .
RUN composer install --prefer-dist --no-scripts --no-progress

# Health check
COPY docker-healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-healthcheck.sh
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD ["docker-healthcheck.sh"]

FROM app AS app_dev
ENV APP_ENV=dev
RUN docker-php-ext-enable xdebug