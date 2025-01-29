<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Get the request path
$request = $_SERVER['REQUEST_URI'];
$path = parse_url($request, PHP_URL_PATH);

// Remove /api prefix
$path = str_replace('/api/', '', $path);

switch ($path) {
    case 'db-status':
        checkDatabaseStatus();
        break;
    default:
        echo json_encode(['message' => 'Welcome to the API!']);
        break;
}

function checkDatabaseStatus()
{
    try {
        $host = getenv('MYSQL_HOST');
        $port = getenv('MYSQL_PORT');
        $db   = getenv('MYSQL_DB');
        $user = getenv('MYSQL_USER');
        $pass = getenv('MYSQL_PASSWORD');

        $dsn = "mysql:host=$host;port=$port;dbname=$db";
        $pdo = new PDO($dsn, $user, $pass);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Get MySQL version
        $stmt = $pdo->query("SELECT VERSION() AS version");
        $version = $stmt->fetch(PDO::FETCH_ASSOC)['version'];

        echo json_encode([
            'success' => true,
            'version' => $version,
            'message' => 'Database connection successful',
            'config' => [
                'host' => $host,
                'port' => $port,
                'database' => $db,
                'user' => $user
            ]
        ]);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => $e->getMessage(),
            'config' => [
                'host' => $host,
                'port' => $port,
                'database' => $db,
                'user' => $user
            ]
        ]);
    }
}
