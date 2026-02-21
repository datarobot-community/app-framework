#!/usr/bin/env bash
# GPG decryption script for .env files
# Used for local development and testing GitHub Actions workflows
#
# This script should be run from the infra/scripts/ directory
# It will decrypt ../../.env.gpg to ../../.env

set -euo pipefail

echo "🔓 Decrypt .env.gpg file"
echo "========================"
echo ""

# Check if .env.gpg exists two levels up (project root)
if [ ! -f ../../.env.gpg ]; then
    echo "❌ Error: .env.gpg file not found in project root"
    echo "Run ./encrypt-secrets.sh first to create it"
    exit 1
fi

# Check if .env already exists
if [ -f ../../.env ]; then
    echo "⚠️  Warning: .env already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 0
    fi (run from infra/, decrypt to parent directory)
echo "Enter your encryption passphrase:"
gpg --quiet --batch --yes --decrypt --output ../.env ../.env.gpg

if [ -f ../ter your encryption passphrase:"
gpg --quiet --batch --yes --decrypt --output .env .env.gpg

if [ -f .env ]; then
    echo ""
    echo "✅ Successfully decrypted .env.gpg → .env"
    echo ""
    echo "⚠️  Remember: Never commit .env to git!"
    echo "   Make sure .env is in your .gitignore"
else
    echo "❌ Error: Decryption failed"
    echo "Check your passphrase and try again"
    exit 1
fi
