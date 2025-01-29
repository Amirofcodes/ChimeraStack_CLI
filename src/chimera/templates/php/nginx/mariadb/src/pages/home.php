<?php

declare(strict_types=1);
$title = 'ChimeraStack PHP Development Environment';
$webPort = $_ENV['NGINX_PORT'] ?? '8093';
$dbPort = $_ENV['MARIADB_PORT'] ?? '3307';
$pmaPort = $_ENV['PHPMYADMIN_PORT'] ?? '8092';
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
                <td>MariaDB <?= $_ENV['DB_DATABASE'] ?></td>
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
                ✓ Connected to MariaDB Server ' . htmlspecialchars($version) . '<br>
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