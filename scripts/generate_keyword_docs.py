#!/usr/bin/env python3
"""Generate HTML keyword documentation from Robot Framework resource files.

Uses libdoc to produce self-contained HTML documentation pages.
Run from the project root: uv run python scripts/generate_keyword_docs.py
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES_DIR = PROJECT_ROOT / "resources"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "keywords"

# Resource files to document (skip saucedemo.resource as it's just imports)
RESOURCE_FILES = [
    "common.resource",
    "login_page.resource",
    "products_page.resource",
    "cart_page.resource",
    "checkout_page.resource",
]


def main():
    """Generate libdoc HTML documentation for all resource files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating keyword documentation...")
    for resource_name in RESOURCE_FILES:
        resource_path = RESOURCES_DIR / resource_name
        if not resource_path.exists():
            print(f"  Skipping {resource_name} (not found)")
            continue

        output_file = OUTPUT_DIR / resource_name.replace(".resource", ".html")
        print(f"  {resource_name} -> {output_file.relative_to(PROJECT_ROOT)}")

        result = subprocess.run(
            [sys.executable, "-m", "robot.libdoc", str(resource_path), str(output_file)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"    Warning: libdoc failed: {result.stderr.strip()}")

    print("Done.")


if __name__ == "__main__":
    main()
