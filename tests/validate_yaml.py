"""
Simple YAML validator that checks basic YAML syntax without requiring PyYAML
"""

import sys
import re


def validate_yaml_file(filepath):
    """Basic YAML validation - checks for common syntax errors"""
    try:
        with open(filepath, "r") as f:
            content = f.read()

        # Check for basic YAML structure
        lines = content.split("\n")

        # Check for proper indentation (YAML uses spaces, not tabs)
        for i, line in enumerate(lines, 1):
            if "\t" in line:
                return False, f"Line {i}: Contains tabs (YAML requires spaces)"

        # Check for proper key-value pairs (key: value)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("#")
                and not stripped.startswith("-")
            ):
                if ":" in stripped:
                    # This looks like a key-value pair
                    parts = stripped.split(":", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        if not key:
                            return False, f"Line {i}: Empty key"

        return True, "Valid YAML structure"

    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def main():
    """Validate all YAML files in the prompts directory"""
    import os

    if len(sys.argv) > 1:
        # Validate specific file
        filepath = sys.argv[1]
        valid, message = validate_yaml_file(filepath)
        print(f"{filepath}: {message}")
        return 0 if valid else 1
    else:
        # Validate all YAML files
        prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        yaml_files = []

        for root, dirs, files in os.walk(prompts_dir):
            for file in files:
                if file.endswith(".yaml"):
                    yaml_files.append(os.path.join(root, file))

        print(f"Found {len(yaml_files)} YAML files to validate\n")

        all_valid = True
        for filepath in sorted(yaml_files):
            valid, message = validate_yaml_file(filepath)
            status = "✓" if valid else "✗"
            print(f"{status} {filepath}: {message}")
            if not valid:
                all_valid = False

        print(f"\n{'=' * 60}")
        if all_valid:
            print(f"✓ All {len(yaml_files)} YAML files are valid!")
        else:
            print(f"✗ Some YAML files have errors")
        print(f"{'=' * 60}")

        return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
