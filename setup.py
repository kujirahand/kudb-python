from setuptools import setup, find_packages
import re
from pathlib import Path

# Read version from pyproject.toml
def get_version():
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        content = pyproject.read_text(encoding='utf-8')
        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
    return "0.0.0"

# get readme
with open("./README.md", encoding='utf-8') as f:
    long_desc = f.read()

AUTHOR = 'kujirahand'
EMAIL = 'web@kujirahand.com'

# setup
setup(
    name="kudb",
    url="https://github.com/kujirahand/kudb",
    description="Simple Document database Library",
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    version=get_version(),
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[],
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ]
)
