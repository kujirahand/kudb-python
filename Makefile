.PHONY: help clean build test deploy deploy-test install dev-install version

help:
	@echo "Available commands:"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make test         - Run tests"
	@echo "  make version      - Show or update version (usage: make version NEW=0.2.5)"
	@echo "  make deploy-test  - Deploy to Test PyPI"
	@echo "  make deploy       - Deploy to PyPI (production)"
	@echo "  make install      - Install package locally"
	@echo "  make dev-install  - Install package in development mode"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf kudb.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

build: clean
	@echo "Generating documentation..."
	python mkdoc.py
	@echo "Building distribution packages..."
	python -m build
	@echo "Build complete! Check dist/ directory"

test:
	@echo "Running doctests..."
	python -m doctest kudb/kudb.py -v
	@echo "Tests complete!"

version:
ifdef NEW
	@python update_version.py $(NEW)
else
	@python update_version.py
endif

deploy-test: build
	@echo "Uploading to Test PyPI..."
	python -m twine upload --repository testpypi dist/*
	@echo "Deployed to Test PyPI!"
	@echo "Install with: pip install --index-url https://test.pypi.org/simple/ kudb"

deploy: build
	@echo "Uploading to PyPI..."
	@read -p "Are you sure you want to deploy to PyPI? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		python -m twine upload dist/*; \
		echo "Deployed to PyPI successfully!"; \
	else \
		echo "Deployment cancelled."; \
	fi

install:
	@echo "Installing package..."
	pip install .

dev-install:
	@echo "Installing package in development mode..."
	pip install -e .
	pip install -r requirements-dev.txt
	@echo "Development environment ready!"

# Check if required tools are installed
check-tools:
	@command -v python >/dev/null 2>&1 || { echo "Python is required but not installed."; exit 1; }
	@python -c "import build" 2>/dev/null || { echo "build is not installed. Run: pip install build"; exit 1; }
	@python -c "import twine" 2>/dev/null || { echo "twine is not installed. Run: pip install twine"; exit 1; }
	@echo "All required tools are installed!"
