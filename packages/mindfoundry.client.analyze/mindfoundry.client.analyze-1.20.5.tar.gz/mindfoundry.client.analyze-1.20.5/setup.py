import os

from setuptools import find_namespace_packages, setup

import versioneer

install_requires = [
    "attrs",
    "httpx>=0.22,<0.23.1",
    "pandas",
    "pyarrow",
    "requests",
]  # etc

dev_extras = [
    "black",
    "check-manifest",
    "coverage",
    "freezegun",
    "isort",
    "mypy",
    "pre-commit",
    "pylint",
    "pytest",
    "pytest-freezegun",
    "pytest-httpx",
    "pylint-pytest",
    "requests_toolbelt",
    "tox",
]

extras_require = {"dev": dev_extras}


# Add a `pip install .[all]` target:
all_extras = set()
for extras_list in extras_require.values():
    all_extras.update(extras_list)
extras_require["all"] = list(all_extras)

version = versioneer.get_version()

project_repo_dir = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(project_repo_dir, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mindfoundry.client.analyze",
    license="MIT",
    version=version,
    cmdclass=versioneer.get_cmdclass(),
    description="Mind Foundry Analyze Python Client",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    # The project"s main homepage.
    url="https://www.mindfoundry.ai/platform",
    # Author details
    author="Mind Foundry Ltd",
    author_email="support@mindfoundry.ai",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",

        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={},
    install_requires=install_requires,
    extras_require=extras_require,
    namespace_packages=["mindfoundry"],
)
