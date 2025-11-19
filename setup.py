"""
StillHere - Setup Configuration

Bringing cherished memories to life through AI-powered photo animation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="stillhere",
    version="0.1.0",
    author="Everett Christman",
    author_email="",  # Add your email if desired
    description="Bringing cherished memories to life through AI-powered photo animation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EverettNC/StillHere",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "flask>=2.3.0",
            "flask-cors>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "stillhere=stillhere.ui.cli:main",
            "stillhere-web=stillhere.ui.web_ui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "stillhere": [
            "models/README.md",
        ],
    },
    keywords="photo animation memory memorial ai deep-learning computer-vision",
    project_urls={
        "Bug Reports": "https://github.com/EverettNC/StillHere/issues",
        "Source": "https://github.com/EverettNC/StillHere",
    },
)
