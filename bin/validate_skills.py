#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-frontmatter",
# ]
# ///
"""
Validate DataRobot skills:
1. All skill folders must start with 'datarobot-'
2. Each skill folder must have a SKILL.md file
3. The 'name' field in SKILL.md frontmatter must match the folder name
"""

import sys
from pathlib import Path
import frontmatter


def validate_skills(repo_root: Path) -> bool:
    """Validate all skills in the repository."""
    errors = []
    skills_found = 0

    # Find all directories that could be skill folders
    for item in repo_root.iterdir():
        if not item.is_dir():
            continue

        # Skip common non-skill directories
        if item.name in {
            ".git",
            ".github",
            "docs",
            "__pycache__",
            ".pytest_cache",
            "bin",
        }:
            continue

        # Check if this looks like a skill folder (has SKILL.md)
        skill_md = item / "SKILL.md"
        if skill_md.exists():
            skills_found += 1
            # This is a skill folder - validate it
            folder_name = item.name

            # Check 1: Folder name must start with 'datarobot-'
            if not folder_name.startswith("datarobot-"):
                errors.append(
                    f"ERROR: Skill folder '{folder_name}' does not start with 'datarobot-'"
                )
                continue

            # Check 2: Parse SKILL.md and check the 'name' field
            try:
                with open(skill_md, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                    skill_name = post.metadata.get("name")

                    if not skill_name:
                        errors.append(
                            f"ERROR: Skill '{folder_name}/SKILL.md' is missing 'name' field in frontmatter"
                        )
                        continue

                    # Check 3: Name in frontmatter must match folder name
                    if skill_name != folder_name:
                        errors.append(
                            f"ERROR: Skill '{folder_name}' has mismatched name in SKILL.md: "
                            f"expected '{folder_name}', got '{skill_name}'"
                        )
            except Exception as e:
                errors.append(f"ERROR: Failed to parse '{folder_name}/SKILL.md': {e}")

    # Check that we found at least one skill
    if skills_found == 0:
        errors.append(
            "ERROR: No skill folders found. Validation script may be running from wrong directory."
        )

    # Print results
    if errors:
        print("❌ Skill validation failed:\n")
        for error in errors:
            print(f"  {error}")
        print()
        return False

    print(f"✅ All skills validated successfully! ({skills_found} skills checked)")
    return True


def main():
    # Script is in bin/, so go up one level to get repo root
    repo_root = Path(__file__).parent.parent
    success = validate_skills(repo_root)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
