from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-model-core",
    install_requires=[
        "marshmallow~=3.0",
        "PyMongo[srv]~=4.0"
    ],
    extras_require={},
)
