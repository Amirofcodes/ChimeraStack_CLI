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
