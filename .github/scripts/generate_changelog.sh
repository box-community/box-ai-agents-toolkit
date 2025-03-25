#!/bin/bash
# Script to generate changelog updates from git commits

set -e

TAG=$1

# Get the last tag
LAST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")

# If no previous tag exists, get all commits
if [ -z "$LAST_TAG" ]; then
    echo "## $TAG - $(date +'%Y-%m-%d')" >CHANGELOG_UPDATES.md
    echo "" >>CHANGELOG_UPDATES.md
    git log --pretty=format:"* %s (%h)" >>CHANGELOG_UPDATES.md
else
    echo "## $TAG - $(date +'%Y-%m-%d')" >CHANGELOG_UPDATES.md
    echo "" >>CHANGELOG_UPDATES.md
    git log --pretty=format:"* %s (%h)" $LAST_TAG..HEAD >>CHANGELOG_UPDATES.md
fi

# Create or update CHANGELOG.md
if [ -f "CHANGELOG.md" ]; then
    # Save the title
    TITLE=$(head -n 2 CHANGELOG.md)

    # Prepend new changes after the title
    echo "$TITLE" >CHANGELOG.md.new
    cat CHANGELOG_UPDATES.md <(echo "") <(tail -n +3 CHANGELOG.md) >>CHANGELOG.md.new
    mv CHANGELOG.md.new CHANGELOG.md
else
    # Create new changelog
    echo "# Changelog" >CHANGELOG.md
    echo "" >>CHANGELOG.md
    cat CHANGELOG_UPDATES.md >>CHANGELOG.md
fi
