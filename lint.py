#!/usr/bin/env python3
"""
Linting script for the Transaction Tracker project.
Run this script to check code quality and formatting.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print("=" * 50)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main function to run all linters."""
    print("🔍 Running linters for Transaction Tracker project...")

    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print(
            "❌ Error: requirements.txt not found. Please run this script from the project root."
        )
        sys.exit(1)

    success = True

    # Run formatters
    success &= run_command(["black", "."], "Black code formatter")
    success &= run_command(["isort", "."], "isort import sorter")

    # Run linters
    success &= run_command(["flake8", "."], "Flake8 style checker")
    success &= run_command(["mypy", "."], "MyPy type checker")

    print(f"\n{'='*50}")
    if success:
        print("🎉 All checks passed! Your code is clean and well-formatted.")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
