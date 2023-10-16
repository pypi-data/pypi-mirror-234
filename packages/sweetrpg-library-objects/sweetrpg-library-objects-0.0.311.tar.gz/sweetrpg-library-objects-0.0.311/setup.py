from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-library-objects",
    install_requires=[
        "Flask~=2.0",
        "marshmallow-jsonapi~=0.24",
        "mongoengine~=0.27",
        "sweetrpg-api-core",
        "sweetrpg-db",
        "sweetrpg-model-core",
    ],
)
