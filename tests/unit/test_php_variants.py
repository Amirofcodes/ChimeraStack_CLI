import importlib
import shutil
from pathlib import Path

import pytest

# Import TemplateManager lazily to avoid heavy dependencies during collection
TemplateManager = importlib.import_module(
    "chimera.core.template_manager").TemplateManager

DB_VARIANTS = [
    "mysql",
    "postgresql",
    "mariadb"
]


@pytest.mark.parametrize("db_variant", DB_VARIANTS)
def test_php_web_db_variants(tmp_path: Path, db_variant: str):
    """Test that PHP web stack properly handles different database variants."""
    tm = TemplateManager(verbose=False)

    # Create a temporary project with specified DB variant
    project_name = f"php-web-{db_variant}-test"
    ok = tm.create_project("stacks/backend/php-web", project_name,
                           target_dir=tmp_path, variant=db_variant)
    assert ok, f"create_project failed for database variant {db_variant}"

    project_dir = tmp_path / project_name

    # Test 1: Ensure docker-compose.yml exists
    compose_path = project_dir / "docker-compose.yml"
    assert compose_path.exists(), "docker-compose.yml not found"

    # Check for absence of variant compose files
    for variant in DB_VARIANTS:
        variant_compose = project_dir / f"docker-compose.{variant}.yml"
        assert not variant_compose.exists(
        ), f"Variant file {variant_compose} should not exist"

    # Test 2: Check docker-compose.yml has the correct database image
    compose_content = compose_path.read_text()

    expected_db_image = {
        "mysql": "mysql:8.0",
        "postgresql": "postgres:15-alpine",
        "mariadb": "mariadb:11"
    }[db_variant]

    assert expected_db_image in compose_content, \
        f"Expected {expected_db_image} in docker-compose.yml for variant {db_variant}"

    # Test 3: Check .env file contains correct database type
    env_path = project_dir / ".env"
    assert env_path.exists(), ".env file not found"

    env_content = env_path.read_text()
    assert f"DB_ENGINE={db_variant}" in env_content, \
        f"Expected DB_ENGINE={db_variant} in .env file"

    # Test 4: Check correct port in .env file
    if db_variant == "postgresql":
        assert "DB_PORT=5432" in env_content, "Expected PostgreSQL port 5432"
    else:
        assert "DB_PORT=3306" in env_content, f"Expected MySQL/MariaDB port 3306 for {db_variant}"

    # Test 5: Check that index.php exists and contains no Jinja placeholders
    index_path = project_dir / "public" / "index.php"
    assert index_path.exists(), "index.php not found in public directory"

    index_content = index_path.read_text()
    assert "{{" not in index_content, "Unresolved Jinja placeholders in index.php"

    # Check db badge color logic works for this variant
    assert db_variant in index_content, f"DB variant {db_variant} not found in index.php"

    # Test 6: Verify DB config exists for the correct variant
    if db_variant == "mysql":
        assert (project_dir / "docker" / "mysql" / "my.cnf").exists(), \
            "MySQL config file not found"
    elif db_variant == "mariadb":
        assert (project_dir / "docker" / "mariadb" / "my.cnf").exists(), \
            "MariaDB config file not found"

    # Test 7: Verify other variant configs were removed
    if db_variant != "mysql":
        assert not (project_dir / "docker" / "mysql" / "my.cnf").exists(), \
            "MySQL config file should be removed for non-MySQL variants"
    if db_variant != "mariadb":
        assert not (project_dir / "docker" / "mariadb" / "my.cnf").exists(), \
            "MariaDB config file should be removed for non-MariaDB variants"

    # Cleanup
    shutil.rmtree(project_dir)
