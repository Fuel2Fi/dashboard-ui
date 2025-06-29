#!/usr/bin/env bash

# Unlock files
echo "Unlocking files to prepare for commit..."
chmod -R u+w . 
echo "All files unlocked."

# Ensure .gitignore excludes the zip
echo "Ensuring .gitignore excludes the backup zip..."
if ! grep -qxF "dashboard-ui-backup.zip" .gitignore; then
  echo "dashboard-ui-backup.zip" >> .gitignore
  echo ".gitignore updated to exclude the backup zip."
fi

# Stop tracking the zip if it was previously committed
if git ls-files --error-unmatch dashboard-ui-backup.zip > /dev/null 2>&1; then
  git rm --cached dashboard-ui-backup.zip
  echo "Removed backup zip from git index."
fi

# Add everything else
echo "Adding all changes to git..."
git add .
git reset dashboard-ui-backup.zip

# Commit
echo "Enter your commit message:"
read commit_message
git commit -m "$commit_message"

# Push
echo "Pushing to origin main branch..."
git push origin main

# Create/update local backup zip
echo "Creating/updating local backup zip..."
zip -r dashboard-ui-backup.zip . -x "*.git*" > /dev/null
echo "Archive created/updated locally (not pushed to GitHub)."

# Lock files again
echo "Locking files back down..."
chmod -R u-w .
echo "✅ Checkpoint complete. Code pushed to GitHub, backup zip saved locally."
