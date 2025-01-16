from setuptools import setup, find_packages

setup(
    name="tarotai",
    version="0.1.0",
    description="A modular Tarot reading and interpretation system with AI enrichment",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/tarotai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "hypothesis>=6.0.0",
            "black>=23.0.0",
        ],
        "ai": [
            "openai>=1.0.0",
            "anthropic>=0.3.0",
        ],
    },
    python_requires=">=3.10",
    include_package_data=True,
    package_data={
        "tarotai": ["data/*.json"],
    },
    entry_points={
        "console_scripts": [
            "tarotai=tarotai.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Fortune Telling",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
