#!/usr/bin/env python3
"""
Version updater script for kudb package
Updates version numbers across all relevant files
"""

import re
import sys
from pathlib import Path


def read_current_version():
    """Read current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)
    
    content = pyproject_path.read_text(encoding='utf-8')
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    return None


def update_file(file_path, pattern, replacement):
    """Update version in a file"""
    path = Path(file_path)
    if not path.exists():
        print(f"Warning: {file_path} not found")
        return False
    
    content = path.read_text(encoding='utf-8')
    new_content = re.sub(pattern, replacement, content)
    
    if content != new_content:
        path.write_text(new_content, encoding='utf-8')
        print(f"✓ Updated {file_path}")
        return True
    else:
        print(f"  No changes needed in {file_path}")
        return False


def update_version(new_version):
    """Update version across all files"""
    print(f"Updating version to {new_version}...\n")
    
    updated_files = []
    
    # Update kudb/__init__.py
    if update_file(
        "kudb/__init__.py",
        r'__version__ = "[^"]+"',
        f'__version__ = "{new_version}"'
    ):
        updated_files.append("kudb/__init__.py")
    
    # Update pyproject.toml
    if update_file(
        "pyproject.toml",
        r'version = "[^"]+"',
        f'version = "{new_version}"'
    ):
        updated_files.append("pyproject.toml")
    
    print(f"\nVersion updated to {new_version}")
    
    if updated_files:
        print("\nNext steps:")
        print("1. Review changes: git diff")
        print(f"2. Commit changes: git add . && git commit -m 'Bump version to {new_version}'")
        print(f"3. Create tag: git tag v{new_version}")
        print("4. Push changes: git push && git push --tags")
        print("5. Deploy to PyPI: make deploy")
    else:
        print("\nNo files were updated.")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        current_version = read_current_version()
        print(f"Current version: {current_version}")
        print("\nUsage: python update_version.py <new_version>")
        print("Example: python update_version.py 0.2.5")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Validate version format (basic check)
    if not re.match(r'^\d+\.\d+\.\d+', new_version):
        print(f"Error: Invalid version format: {new_version}")
        print("Version should be in format: X.Y.Z (e.g., 0.2.5)")
        sys.exit(1)
    
    current_version = read_current_version()
    if current_version:
        print(f"Current version: {current_version}")
    
    # Confirm update
    response = input(f"\nUpdate version from {current_version} to {new_version}? (y/n): ")
    if response.lower() != 'y':
        print("Update cancelled.")
        sys.exit(0)
    
    update_version(new_version)


if __name__ == "__main__":
    main()
