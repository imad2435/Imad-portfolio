#!/bin/bash

# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# (Optional) Apply database migrations
# Note: Vercel builds are ephemeral. For a real database, you'd run
# migrations as a separate step or from your local machine.
# We will run it here to ensure the build completes successfully.
python manage.py migrate