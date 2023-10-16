# -*- coding: utf-8 -*-
"""Setuptools script for app."""
from setuptools import setup

from procustodibus_agent import __version__ as version

with open("README.md") as f:
    description = f.read()

with open("requirements/prod.txt") as f:
    requirements = f.read().splitlines()

with open("requirements/lint.txt") as f:
    requirements_lint = f.read().splitlines()

with open("requirements/test.txt") as f:
    requirements_test = f.read().splitlines()

setup(
    name="procustodibus_agent",
    version=version,
    description="Synchronizes your WireGuard settings with Pro Custodibus.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://www.procustodibus.com/",
    project_urls={
        "Changelog": "https://docs.procustodibus.com/guide/agents/download/#changelog",
        "Documentation": "https://docs.procustodibus.com/guide/agents/run/",
        "Source": "https://git.sr.ht/~arx10/procustodibus-agent",
        "Tracker": "https://todo.sr.ht/~arx10/procustodibus-agent",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    license="MIT",
    author="Arcem Tene",
    author_email="dev@arcemtene.com",
    packages=[
        "procustodibus_agent",
        "procustodibus_agent.mfa",
    ],
    entry_points={
        "console_scripts": [
            "procustodibus-agent = procustodibus_agent.cli:main",
            "procustodibus-credentials = procustodibus_agent.credentials:main",
            "procustodibus-mfa = procustodibus_agent.mfa.cli:main",
        ],
    },
    install_requires=requirements,
    extras_require={"lint": requirements_lint, "test": requirements_test},
    python_requires=">=3.6",
    zip_safe=True,
)
