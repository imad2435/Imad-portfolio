#!/bin/bash

# Exit on error
set -e

# Build the project
python manage.py collectstatic --no-input
python manage.py migrate