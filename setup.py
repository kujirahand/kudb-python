from setuptools import setup, find_packages
from kudb import __version__ # バージョン情報取得のため

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
    version=__version__,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
