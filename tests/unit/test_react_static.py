import os
import tempfile
import unittest
from pathlib import Path

import pytest

from chimera.core.template_manager import TemplateManager


class TestReactStaticTemplate(unittest.TestCase):
    """Test that frontend/react-static template renders correctly."""

    def setUp(self):
        """Set up temporary directory for project creation."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_react_static_template(self):
        """Test that the React static template creates expected files."""
        # Create project
        template_manager = TemplateManager()
        project_name = "react-test"
        project_path = self.project_path / project_name

        template_manager.create_project(
            template="stacks/frontend/react-static",
            name=project_name,
            output_dir=self.project_path,
        )

        # Check docker-compose.yml exists and contains only frontend service
        compose_file = project_path / "docker-compose.yml"
        assert compose_file.exists(), "docker-compose.yml should exist"

        compose_content = compose_file.read_text()
        assert "frontend:" in compose_content, "docker-compose.yml should contain frontend service"
        assert "nginx:" in compose_content, "docker-compose.yml should contain nginx service"
        assert "db:" not in compose_content, "docker-compose.yml should not contain db service"

        # Check .env file exists and contains FRONTEND_PORT
        env_file = project_path / ".env"
        assert env_file.exists(), ".env file should exist"

        env_content = env_file.read_text()
        assert "FRONTEND_PORT" in env_content, ".env should contain FRONTEND_PORT"
        assert "VITE_BACKEND_URL" in env_content, ".env should contain VITE_BACKEND_URL"

        # Check welcome.html exists
        welcome_file = project_path / "public" / "welcome.html"
        assert welcome_file.exists(), "welcome.html should exist"

        # Check frontend files exist
        assert (project_path / "frontend" / "vite.config.ts").exists()
        assert (project_path / "frontend" / "tailwind.config.js").exists()
        assert (project_path / "frontend" / "src" / "App.tsx").exists()
        assert (project_path / "frontend" / "src" / "main.tsx").exists()
        assert (project_path / "frontend" / "src" / "index.css").exists()

        # Check Nginx config exists
        assert (project_path / "docker" / "nginx" /
                "conf.d" / "default.conf").exists()

        # Check Dockerfile exists and contains Vite dev command
        dockerfile = project_path / "Dockerfile"
        assert dockerfile.exists(), "Dockerfile should exist"

        dockerfile_content = dockerfile.read_text()
        assert "npm run dev" in dockerfile_content, "Dockerfile should use Vite dev server"
        assert "npm run build" in dockerfile_content, "Dockerfile should include build step"
