#!/bin/bash

echo "Unlocking files to prepare for commit..."
./lock.sh unlock

echo "Adding all changes to git..."
git add .

echo "Enter your commit message:"
read commit_msg

if [ -z "$commit_msg" ]; then
  echo "Commit message cannot be empty. Aborting."
  exit 1
fi

echo "Committing changes..."
git commit -m "$commit_msg"

echo "Pushing to origin main branch..."
git push origin main

echo "Creating/updating backup zip..."
zip -r -FS dashboard-ui-backup.zip dashboard-ui

echo "Locking files back down..."
./lock.sh lock

echo "Checkpoint saved and backed up successfully."
