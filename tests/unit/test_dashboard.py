import importlib
import shutil
from pathlib import Path

import pytest

# Import TemplateManager lazily to avoid heavy dependencies during collection
TemplateManager = importlib.import_module(
    "chimera.core.template_manager").TemplateManager

TEMPLATES_TO_TEST = [
    ("stacks/backend/php-web", "mysql"),
    ("stacks/fullstack/react-php", None),
    ("stacks/frontend/react-static", None),
]


@pytest.mark.parametrize("template_id,variant", TEMPLATES_TO_TEST)
def test_dashboard_generation(tmp_path: Path, template_id: str, variant: str):
    """Test that the welcome dashboard is properly generated in each template."""
    tm = TemplateManager(verbose=False)

    # Create a temporary project
    project_name = f"{Path(template_id).name}-test"
    ok = tm.create_project(template_id, project_name,
                           target_dir=tmp_path, variant=variant)
    assert ok, f"create_project failed for {template_id}"

    project_dir = tmp_path / project_name

    # Ensure welcome.html exists
    welcome_path = project_dir / "www" / "welcome.html"
    assert welcome_path.exists(), f"welcome.html not found in {template_id}"

    # Check content of welcome.html
    welcome_content = welcome_path.read_text()

    # Verify no unresolved Jinja2 templates (no "{{" tokens)
    assert "{{" not in welcome_content, f"Unresolved template variables in {welcome_path}"

    # Verify essential elements are present
    assert "<title>" in welcome_content, "Title tag missing in welcome.html"
    assert "cdn.tailwindcss.com" in welcome_content, "Tailwind CDN missing in welcome.html"
    assert "Available Services" in welcome_content, "Services section missing in welcome.html"

    # Check if docker-compose.yml has the correct nginx configuration
    compose_path = project_dir / "docker-compose.yml"
    compose_content = compose_path.read_text()

    # Verify nginx-proxy mounts /usr/share/nginx/html
    assert "/usr/share/nginx/html" in compose_content, \
        "Nginx proxy not configured to mount /usr/share/nginx/html"

    # Cleanup to keep tmp dir small
    shutil.rmtree(project_dir)
