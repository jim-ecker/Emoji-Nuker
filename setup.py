#!/usr/bin/env python3
"""
Setup script for emoji-nuker
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read the version from the script
def get_version():
    # For now, use a simple version
    return "1.0.0"

setup(
    name="emoji-nuker",
    version=get_version(),
    description="Remove emojis from code files in a project directory",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["emoji_lut"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "emoji-nuker=emoji_nuker:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Tools",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    keywords="emoji, unicode, text-processing, code-cleanup, development-tools",
    project_urls={
        "Source": "https://github.com/your-username/emoji-nuker",
        "Bug Reports": "https://github.com/your-username/emoji-nuker/issues",
    },
) 