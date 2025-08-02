"""
Setup script for FolderPulse application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "A comprehensive Python application for file system monitoring and management."

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f.readlines() 
            if line.strip() and not line.startswith("#")
        ]
else:
    requirements = [
        "flask>=2.3.0",
        "flask-socketio>=5.3.0",
        "watchdog>=3.0.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0"
    ]

setup(
    name="folderpulse",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive Python application for file system monitoring and management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/folderpulse",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Filesystems",
        "Topic :: System :: Monitoring",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "build": [
            "pyinstaller>=5.13.0",
            "setuptools>=68.0.0",
            "wheel>=0.41.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "folderpulse=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml", "*.txt", "*.md"],
        "assets": ["*"],
        "config": ["*.json"],
    },
    zip_safe=False,
)
