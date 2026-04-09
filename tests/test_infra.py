import os
import subprocess


def test_workflow_syntax():
    workflow_path = ".github/workflows/python-package.yml"
    assert os.path.exists(workflow_path)
    # Simple check for required keys
    with open(workflow_path, 'r') as f:
        content = f.read()
        assert "name:" in content
        assert "on:" in content
        assert "jobs:" in content


def test_population_script_execution():
    # Verify the script runs without error
    result = subprocess.run(
        ["python3", "scripts/populate_manifold.py"],
        env={**os.environ, "PYTHONPATH": "src"},
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "[POPULATE] Manifold population complete." in result.stdout


def test_docs_existence():
    assert os.path.exists("docs/infrastructure/setup.md")
    with open("docs/infrastructure/setup.md", 'r') as f:
        content = f.read()
        assert "# STRATOS-OS Infrastructure Setup" in content
