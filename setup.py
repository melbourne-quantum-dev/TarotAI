from setuptools import setup, find_packages

setup(
    name="tarotai",
    version="0.1.0",
    description="A modular Tarot reading and interpretation system with AI enrichment",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/melbourne-quantum-dev/tarotai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "anthropic>=0.3.0,<1.0.0",
        "rich>=13.0.0,<14.0.0",
        "typer[all]>=0.9.0,<1.0.0",
        "questionary>=2.0.0,<3.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "typing-extensions>=4.1.1,<5.0.0",
        "openai>=1.0.0,<2.0.0",
        "voyageai>=0.3.0,<1.0.0",
        "realtimestt>=0.3.93,<1.0.0",
        "realtimetts[system]==0.4.40",
        "elevenlabs>=1.50.3,<2.0.0",
        "pyttsx3>=2.98,<3.0.0",
        "PyPDF2>=3.0.0,<4.0.0",
        "httpx>=0.25.0,<1.0.0",
        "uv>=0.1.0,<1.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "ai": [
            "openai>=1.0.0",
            "voyageai>=0.3.0",
        ],
    },
    python_requires=">=3.10",
    include_package_data=True,
    package_data={
        "tarotai": ["data/*.json", "data/*.pdf"],
    },
    entry_points={
        "console_scripts": [
            "tarotai=tarotai.cli:app",
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
