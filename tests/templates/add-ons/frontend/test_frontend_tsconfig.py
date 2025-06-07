"""Test tsconfig.json template validation."""

import json
from pathlib import Path


def test_tsconfig_template_contains_modern_typescript_options():
    """Test that the tsconfig.json template contains modern TypeScript configurations."""
    # Path to the tsconfig.json template file
    template_root = Path(__file__).parent.parent.parent.parent.parent
    tsconfig_template_path = (
        template_root / 
        "templates" / 
        "add-ons" / 
        "frontend" / 
        "{{ cookiecutter.__folder_name }}" / 
        "packages" / 
        "{{ cookiecutter.frontend_addon_name }}" / 
        "tsconfig.json"
    )
    
    assert tsconfig_template_path.exists(), f"tsconfig.json template should exist at {tsconfig_template_path}"
    
    # Read and parse the tsconfig.json template
    with open(tsconfig_template_path, 'r') as f:
        tsconfig_content = json.load(f)
    
    # Validate basic structure
    assert "compilerOptions" in tsconfig_content, "compilerOptions should be present in tsconfig.json"
    
    compiler_options = tsconfig_content["compilerOptions"]
    
    # Test for modern TypeScript options
    assert "moduleDetection" in compiler_options, (
        "moduleDetection should be present in compilerOptions"
    )
    assert compiler_options["moduleDetection"] == "force", (
        "moduleDetection should be set to 'force'"
    )
    
    assert "verbatimModuleSyntax" in compiler_options, (
        "verbatimModuleSyntax should be present in compilerOptions"
    )
    assert compiler_options["verbatimModuleSyntax"] is True, (
        "verbatimModuleSyntax should be set to true"
    )
    
    # Also validate other expected TypeScript configurations
    expected_options = {
        "allowJs": True,
        "noEmit": True, # Prevent emitting output files
    }
    
    for option, expected_value in expected_options.items():
        assert option in compiler_options, f"{option} should be present in compilerOptions"
        assert compiler_options[option] == expected_value, (
            f"{option} should be set to {expected_value}, but got {compiler_options[option]}"
        )


def test_tsconfig_template_include_patterns():
    """Test that tsconfig.json has proper include patterns."""
    template_root = Path(__file__).parent.parent.parent.parent.parent
    tsconfig_template_path = (
        template_root / 
        "templates" / 
        "add-ons" / 
        "frontend" / 
        "{{ cookiecutter.__folder_name }}" / 
        "packages" / 
        "{{ cookiecutter.frontend_addon_name }}" / 
        "tsconfig.json"
    )
    
    with open(tsconfig_template_path, 'r') as f:
        tsconfig_content = json.load(f)
    
    # Test include patterns
    assert "include" in tsconfig_content, "include should be present in tsconfig.json"
    include_patterns = tsconfig_content["include"]
    expected_includes = ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
    
    for pattern in expected_includes:
        assert pattern in include_patterns, f"Include pattern {pattern} should be present"
