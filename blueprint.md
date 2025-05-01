# Blueprint

## System Architecture Overview

dockerized full-stack application with clear separation of concerns:

1. **Frontend**: React/TypeScript/Tailwind CSS application
2. **Backend**: PHP RESTful API with MVC architecture
3. **Database**: MySQL 8.0
4. **Web Server**: Nginx serving as reverse proxy
5. **Admin Tools**: phpMyAdmin for database management

The system is fully containerized using Docker, with each service running in its own container and communicating through a Docker network.

## Deployment Architecture

```
┌─────────────────────────────────── VPS Host ──────────────────────────────────┐
│                                                                                │
│  ┌──────────────────────────── Docker Environment ───────────────────────────┐│
│  │                                                                           ││
│  │  ┌─────────────────┐    ┌────────────────────┐    ┌────────────────────┐  ││
│  │  │  Nginx Container│    │ Frontend Container │    │ Backend Container  │  ││
│  │  │  Reverse Proxy  │    │ React Application  │    │ PHP 8.1 API        │  ││
│  │  │  SSL Termination│    │ Built with Vite    │    │ RESTful Services   │  ││
│  │  │  Ports: 80, 443 │    │ Served via Nginx   │    │ Served via Nginx   │  ││
│  │  └─────────────────┘    └────────────────────┘    └────────────────────┘  ││
│  │                                                                           ││
│  │  ┌─────────────────┐    ┌────────────────────┐                            ││
│  │  │ MySQL Container │    │ phpMyAdmin         │                            ││
│  │  │ MySQL 8.0       │    │ Database Admin     │                            ││
│  │  │ Persistent Data │    │ Protected Access   │                            ││
│  │  │ Volume: mysql_data   │ Connected to MySQL │                            ││
│  │  └─────────────────┘    └────────────────────┘                            ││
│  │                                                                           ││
│  └───────────────────────────────────────────────────────────────────────────┘│
                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### MVC Structure

The PHP backend follows a clean MVC pattern:

```
┌─────────────────── API Entry Point ──────────────────┐
│                     index.php                         │
│    Router Principal handling URL routing logic        │
└──────────────────────┬────────────────────────────────┘
                       │
                       ▼
┌─────────────────── Controllers ──────────────────────┐
│ ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│ │ AuthController│ │UserController│ ResourceController │
│ └─────────────┘ └──────────────┘ └─────────────────┘ │
│ ┌─────────────┐                                      │
│ │PaymentController                                    │
│ └─────────────┘                                      │
└───────────────────────┬──────────────────────────────┘
                       │
       ┌───────────────┴───────────────┐
       │                               │
       ▼                               ▼
┌──── Models ─────┐         ┌──── Core Services ─────┐
│ ┌────────────┐  │         │ ┌───────────────┐      │
│ │ User Model │  │         │ │ JWT Service   │      │
│ └────────────┘  │         │ └───────────────┘      │
│ ┌────────────┐  │         │ ┌───────────────┐      │
│ Resource Model│  │         │ │Response Format│      │
│ └────────────┘  │         │ └───────────────┘      │
│ ┌────────────┐  │         │ ┌───────────────┐      │
│ │Payment Model│  │         │ │Database Service      │
│ └────────────┘  │         │ └───────────────┘      │
└─────────────────┘         └──────────────────────┘
                                      │
                                      ▼
                           ┌──── Database ─────┐
                           │     MySQL 8.0     │
                           └──────────────────┘
```

### Core Components

1. **Router (index.php)**: Central entry point handling URL routing and API endpoint dispatching
2. **Controllers**: Handle business logic and direct traffic between models and responses
3. **Models**: Represent data entities and contain database operations
4. **Core Services**:
   - JWT authentication
   - Database connectivity
   - Response formatting
   - Request parsing

## Frontend Architecture

```
┌───────────────── React Application ────────────────┐
│                      App.tsx                        │
└───────────────────────┬────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌──── Pages ──────┐           ┌──── Context API ─────┐
│ Dashboard       │           │ ┌───────────────┐    │
│ Resources       │           │ │ Auth Context  │    │
│ Auth Pages      │           │ └───────────────┘    │
│ User Profile    │           │ ┌───────────────┐    │
└─────────────────┘           │ │ Theme Context │    │
                              │ └───────────────┘    │
                              └─────────────────────┘
                                        │
                  ┌─────────────────────┴────────────────────┐
                  │                                          │
                  ▼                                          ▼
┌──────────── Components ────────────┐    ┌──────────── Services ─────────────┐
│ Reusable UI Components             │    │ ┌─────────────┐ ┌────────────────┐│
│ Forms, Buttons, Layouts            │    │ │API Service  │ Resource Service ││
│ Cards, Navigation                  │    │ └─────────────┘ └────────────────┘│
└──────────────────────────────────┘    │ ┌─────────────┐ ┌────────────────┐│
                                         │ │Auth Service │ │Payment Service  ││
                                         │ └─────────────┘ └────────────────┘│
                                         └───────────────────────────────────┘
```

### Key Features

1. **Context API** for state management
2. **Service Modules** for API communication
3. **TypeScript** for type safety
4. **Tailwind CSS** for styling
5. **Component-based** architecture

## Database Schema

The MySQL database consists of the following primary tables:

1. **users**: User authentication and profile data
2. **Resources**: Available resources
3. **resource_downloads**: Records of resource downloads by users
4. **payments**: Payment transactions
5. **password_reset_tokens**: Password reset functionality

## CI/CD Pipeline

The project includes Docker configurations for both development and production environments:

- Development: `docker-compose.yml`
- Production: `docker-compose.prod.yml`

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **SSL Termination**: HTTPS support via Nginx
3. **Password Hashing**: Secure password storage
4. **Protected Routes**: Authorization middleware
5. **CORS Protection**: Configured in both Nginx and PHP

## ChimeraStack CLI Integration Blueprint

For creating a minimal template for the ChimeraStack CLI, the following structure is recommended:

```
chimera-stack-template/
├── docker/
│   ├── frontend/
│   │   ├── Dockerfile.dev
│   │   └── Dockerfile.prod
│   ├── backend/
│   │   ├── Dockerfile.dev
│   │   └── Dockerfile.prod
│   └── nginx/
│       ├── conf/
│       │   └── default.conf.template
│       └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── core/
│   │   └── index.php
│   └── composer.json
├── database/
│   └── init/
│       └── schema.sql
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

## Key Template Components for ChimeraStack CLI

1. **Base Infrastructure**:

   - Docker Compose for service orchestration
   - Nginx configuration for reverse proxy
   - Database initialization scripts

2. **Minimal Backend**:

   - PHP MVC structure with core components
   - Basic authentication system
   - RESTful API foundation

3. **Minimal Frontend**:

   - React/TypeScript starter with Tailwind CSS
   - Service layer for API communication
   - Authentication context for state management

4. **Development Utilities**:
   - Hot-reloading for frontend and backend
   - Database admin interface
   - Environment variable templates

## Recommendations for ChimeraStack CLI Integration

1. **Templating Engine**: Implement a template engine to substitute project-specific variables (project name, ports, etc.)

2. **Configuration Generator**: Create a command to generate configuration files based on user preferences

3. **Environment Detection**: Include logic to detect available ports and suggest default configurations

4. **Documentation**: Provide clear documentation on extending the template for different use cases

5. **Cleanup Script**: Include a script to remove example code and reset to a truly minimal state after scaffolding
