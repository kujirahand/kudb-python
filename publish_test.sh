#!/bin/bash
rm -f -r dist
rm -f -r build
rm -f -r kudb.egg-info

python3 setup.py sdist
python3 setup.py bdist_wheel

twine upload --repository testpypi dist/*
echo "if ok:"
echo "  twine upload --repository pypi dist/*"

