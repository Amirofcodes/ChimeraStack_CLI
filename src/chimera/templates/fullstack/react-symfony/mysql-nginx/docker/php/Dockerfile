FROM php:8.3-fpm-alpine AS app

RUN apk add --no-cache \
    acl \
    autoconf \
    build-base \
    linux-headers \
    fcgi \
    file \
    gettext \
    git \
    gnu-libiconv \
    bash \
    icu-dev \
    libzip-dev \
    nodejs \
    npm \
    $PHPIZE_DEPS

RUN docker-php-ext-configure zip \
    && docker-php-ext-install -j$(nproc) \
    intl \
    zip \
    pdo_mysql \
    && pecl install \
    apcu \
    xdebug \
    && pecl clear-cache \
    && docker-php-ext-enable \
    apcu \
    opcache

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Create required directories
RUN mkdir -p \
    var/cache \
    var/log \
    var/sessions \
    /var/log/php \
    && chmod -R 777 var

WORKDIR /var/www/html

COPY php.ini /usr/local/etc/php/conf.d/
COPY www.conf /usr/local/etc/php-fpm.d/

COPY docker-healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-healthcheck.sh

HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD ["docker-healthcheck.sh"]

FROM app AS app_dev
ENV APP_ENV=dev
RUN docker-php-ext-enable xdebug