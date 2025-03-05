"""Tests for documentation_addon template generation."""

from pathlib import Path
from .conftest import EXPECTED_FILES

import pytest


def test_default_bake(bake_template, default_context, tmp_path):
    """Test baking with default context succeeds and initializes Git."""
    output_dir = bake_template(default_context, tmp_path)
    assert output_dir.exists(), "Output directory was not created"
    assert output_dir.name == default_context["__folder_name"], "Folder name mismatch"
    assert (output_dir / ".git").exists(), "Git was not initialized"


def test_no_git_bake(bake_template, no_git_context, tmp_path):
    """Test baking without Git initialization succeeds."""
    output_dir = bake_template(no_git_context, tmp_path)
    assert output_dir.exists(), "Output directory was not created"
    assert output_dir.name == no_git_context["__folder_name"], "Folder name mismatch"
    assert not (output_dir / ".git").exists(), "Git was initialized unexpectedly"


def test_variable_substitution(bake_template, default_context, tmp_path):
    """Test that all Jinja2 variables are substituted in the output."""
    output_dir = bake_template(default_context, tmp_path)
    text_extensions = [".md", ".txt", ".py", ".rst", ".json", ".xml", ".yaml", ".ini"]
    for file_path in output_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in text_extensions:
            content = file_path.read_text(encoding="utf-8")
            assert "{{" not in content, f"Unsubstituted variable found in {file_path}"


def test_file_generation(bake_template, default_context, tmp_path):
    """Test that all expected files are generated."""
    output_dir = bake_template(default_context, tmp_path)
    for file_path in EXPECTED_FILES:
        assert (output_dir / file_path).exists(), f"Missing file: {file_path}"


def test_post_gen_hook(bake_template, default_context, tmp_path):
    """Test that the post-generation hook runs correctly (Git init)."""
    output_dir = bake_template(default_context, tmp_path)
    assert (output_dir / ".git").exists(), "Git repository was not initialized"
