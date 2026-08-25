#!/usr/bin/env python3
"""
Increments the version number in package.json, creates a PR, merges it,
tags the merge commit, and creates a GitHub release.

Designed to run inside GitHub Actions (workflow_dispatch triggered via
`gh workflow run release.yml`).

Requires: gh CLI authenticated with GITHUB_TOKEN (set as GH_TOKEN env var).
"""

import json
import datetime
import os
import subprocess
import sys

# --- Configuration ---
FILE_PATH = 'package.json'
REPO_NAME = 'magenbrot/Feuerwehr-Beitrag-Generator'
MAIN_BRANCH = 'main'


def get_new_version(old_version):
    """
    Calculates the new version based on YYYY.MM.PATCH logic.
    """
    current_year_month = datetime.date.today().strftime('%Y.%m')
    parts = old_version.split('.')

    if len(parts) == 3:
        old_year_month = f"{parts[0]}.{parts[1]}"
        try:
            old_patch = int(parts[2])
            if old_year_month == current_year_month:
                return f"{current_year_month}.{old_patch + 1:02d}"
        except ValueError:
            pass

    return f"{current_year_month}.00"


def run_command(command, description):
    """
    Executes a shell command using subprocess.
    """
    print(f"\n-> {description}")
    print(f"   Command: {' '.join(command)}")

    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        cwd='.'
    )
    print("   [OK]")
    if result.stdout:
        print(f"   Stdout:\n{result.stdout.strip()}")
    return result


def main():
    """
    Main orchestration: version bump → branch → PR → merge → tag → release.
    """
    try:
        # Step 1: Calculate new version
        if not os.path.exists(FILE_PATH):
            print(f"Error: {FILE_PATH} not found.")
            sys.exit(1)

        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)

        old_version = data.get('version', '0.0.0')
        new_version = get_new_version(old_version)
        tag_name = new_version

        print(f"Old version: {old_version} -> New version: {new_version}")

        # Step 2: Create release branch FIRST (before modifying anything)
        branch_name = f"release/{new_version}"
        run_command(['git', 'checkout', '-b', branch_name], f"Creating branch {branch_name}")

        # Step 3: Update version in package.json
        data['version'] = new_version
        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        # Step 4: Commit and push the version bump
        run_command(['git', 'add', FILE_PATH], f"Staging {FILE_PATH}")
        run_command(['git', 'commit', '-m', f'Release {new_version}'], "Creating commit")
        run_command(['git', 'push', 'origin', branch_name], f"Pushing branch {branch_name}")

        # Step 5: Create PR
        pr_result = run_command(
            ['gh', 'pr', 'create',
             '--repo', REPO_NAME,
             '--base', MAIN_BRANCH,
             '--head', branch_name,
             '--title', f'Release {new_version}',
             '--body', f'Automated version bump to {new_version}'],
            "Creating PR"
        )

        # Extract PR number from gh output
        pr_number = pr_result.stdout.strip().split('/')[-1]
        print(f"   PR number: {pr_number}")

        # Step 5: Merge PR (squash to keep history clean)
        run_command(
            ['gh', 'pr', 'merge', pr_number,
             '--repo', REPO_NAME,
             '--squash',
             '--delete-branch'],
            "Merging PR"
        )

        # Step 6: Switch back to main and sync with remote (avoid merge commits)
        run_command(['git', 'checkout', MAIN_BRANCH], "Switching to main")
        run_command(['git', 'reset', '--hard', f'origin/{MAIN_BRANCH}'], "Syncing with remote main")

        # Step 7: Fetch remote, tag the merge commit, push tag
        run_command(['git', 'fetch', 'origin'], "Fetching remote")
        run_command(['git', 'tag', tag_name, f'origin/{MAIN_BRANCH}'], f"Creating tag {tag_name} on remote main")
        run_command(['git', 'push', 'origin', tag_name], f"Pushing tag {tag_name}")

        # Step 8: Create GitHub release (triggers docker-image.yml)
        run_command(
            ['gh', 'release', 'create', tag_name,
             '--repo', REPO_NAME,
             f'--title=Feuerwehr-Beitrag-Generator {tag_name}',
             '--generate-notes'],
            "Creating GitHub release"
        )

        print("\n" + "="*50 + "\nRelease published successfully!\n" + "="*50)

    except subprocess.CalledProcessError as err:
        print(f"\nCommand failed: {err.stderr}")
        sys.exit(1)
    except Exception as err:  # pylint: disable=broad-except
        print(f"\nAn error occurred: {err}")
        sys.exit(1)


if __name__ == '__main__':
    main()
