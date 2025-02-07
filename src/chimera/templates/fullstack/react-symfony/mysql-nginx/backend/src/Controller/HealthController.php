<?php

namespace App\Controller;

use Doctrine\DBAL\Connection;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/api/health')]
class HealthController extends AbstractController
{
    #[Route('', name: 'health_check', methods: ['GET'])]
    public function check(): JsonResponse
    {
        return new JsonResponse(['status' => 'healthy']);
    }

    #[Route('/db', name: 'db_health_check', methods: ['GET'])]
    public function checkDatabase(Connection $connection): JsonResponse
    {
        try {
            $version = $connection->executeQuery('SELECT VERSION()')->fetchOne();

            return new JsonResponse([
                'success' => true,
                'version' => $version,
                'config' => [
                    'host' => $connection->getParams()['host'],
                    'port' => $connection->getParams()['port'] ?? 3306,
                    'database' => $connection->getParams()['dbname'],
                    'user' => $connection->getParams()['user'],
                ]
            ]);
        } catch (\Exception $e) {
            return new JsonResponse([
                'success' => false,
                'message' => $e->getMessage(),
                'config' => [
                    'host' => $connection->getParams()['host'],
                    'port' => $connection->getParams()['port'] ?? 3306,
                    'database' => $connection->getParams()['dbname'],
                    'user' => $connection->getParams()['user'],
                ]
            ], 500);
        }
    }
}
