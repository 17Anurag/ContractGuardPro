# Legal Contract Assistant - Makefile
# Common tasks for development and deployment

.PHONY: help setup install test run clean lint format

# Default target
help:
	@echo "Legal Contract Assistant - Available Commands:"
	@echo ""
	@echo "  setup     - Complete setup (install dependencies, download models)"
	@echo "  install   - Install Python dependencies only"
	@echo "  test      - Run system tests"
	@echo "  run       - Launch the application"
	@echo "  clean     - Clean temporary files and logs"
	@echo "  lint      - Run code linting"
	@echo "  format    - Format code with black"
	@echo ""
	@echo "Quick start: make setup && make run"

# Complete setup
setup:
	@echo "🚀 Setting up Legal Contract Assistant..."
	python setup.py

# Install dependencies only
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

# Run system tests
test:
	@echo "🧪 Running system tests..."
	python test_system.py

# Launch application
run:
	@echo "🚀 Launching application..."
	python run.py

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf .pytest_cache/
	rm -rf temp_documents/*
	rm -f logs/test_audit.log
	rm -f test_contract.txt
	@echo "✅ Cleanup completed"

# Code linting (optional)
lint:
	@echo "🔍 Running code linting..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ app.py --max-line-length=120 --ignore=E203,W503; \
	else \
		echo "⚠️  flake8 not installed. Run: pip install flake8"; \
	fi

# Code formatting (optional)
format:
	@echo "✨ Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black src/ app.py --line-length=120; \
	else \
		echo "⚠️  black not installed. Run: pip install black"; \
	fi

# Development setup with additional tools
dev-setup: setup
	@echo "🛠️  Installing development tools..."
	pip install black flake8 pytest
	@echo "✅ Development environment ready"

# Quick health check
health:
	@echo "🏥 System health check..."
	@python -c "import sys; print(f'Python: {sys.version}')"
	@python -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
	@python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy: ✅')"
	@echo "✅ System appears healthy"

# Show system information
info:
	@echo "ℹ️  Legal Contract Assistant Information"
	@echo "======================================"
	@echo "Purpose: Educational contract analysis for Indian SMEs"
	@echo "Disclaimer: Not legal advice - educational use only"
	@echo "Features: Risk analysis, plain language explanations, templates"
	@echo "Requirements: Python 3.8+, 2GB RAM, Internet for LLM APIs"
	@echo "Privacy: Local processing, no permanent storage by default"
	@echo "======================================"