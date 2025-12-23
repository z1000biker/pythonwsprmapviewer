# Makefile for WSPR Band Spot Viewer

PYTHON = python
PIP = pip
APP = wsprbandmapviewer.py

.PHONY: install run clean help

help:
	@echo "Usage:"
	@echo "  make install    Install dependencies"
	@echo "  make run        Run the application"
	@echo "  make clean      Remove temporary files"

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(APP)

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
