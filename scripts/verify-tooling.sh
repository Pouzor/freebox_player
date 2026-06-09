#!/bin/bash
set -e

echo "Verifying project tooling..."

# Python
if command -v python3 &> /dev/null; then
  echo "✓ Python: $(python3 --version)"
else
  echo "✗ Python3 not installed"
  exit 1
fi

# Ruff
if command -v ruff &> /dev/null; then
  echo "✓ Ruff installed"
else
  echo "⚠ Ruff not installed. Run: pip install ruff"
fi

# pre-commit
if command -v pre-commit &> /dev/null; then
  echo "✓ pre-commit installed"
else
  echo "⚠ pre-commit not installed. Run: pip install pre-commit && pre-commit install"
fi

# GitHub CLI
if command -v gh &> /dev/null; then
  if gh auth status &> /dev/null; then
    echo "✓ GitHub CLI authenticated"
  else
    echo "✗ GitHub CLI not authenticated. Run: gh auth login"
  fi
else
  echo "⚠ GitHub CLI not installed. Run: brew install gh"
fi

echo ""
echo "Tooling verification complete!"
