#!/bin/bash
echo "Locking all project files..."
chmod -R u-w .
echo "Done. All files locked (read-only)."
