#!/bin/bash

if [ "$1" == "lock" ]; then
  echo "Locking all files and folders (removing write permissions)..."
  chmod -R a-w .
  echo "All files and folders locked."
elif [ "$1" == "unlock" ]; then
  echo "Unlocking all files and folders (restoring write permissions for user)..."
  chmod -R u+w .
  echo "All files and folders unlocked."
else
  echo "Usage: ./lock.sh [lock|unlock]"
  echo "Example: ./lock.sh lock   # to lock files and folders"
  echo "         ./lock.sh unlock # to unlock files and folders"
fi
