#!/bin/bash
set -e
/home/jasper/eirene-projects/04-forge/.venv/bin/python -m pytest tests/ -v --tb=short
