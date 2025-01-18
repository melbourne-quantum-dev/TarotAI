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
    packages=find_packages(where="src", include=["tarotai*"]),
    package_dir={"": "src"},
    install_requires=[
        "anthropic>=0.39.0",
        "elevenlabs>=1.50.3",
        "fastapi>=0.109.0",
        "httpx>=0.27.0",
        "Pillow>=10.0.0",
        "PyPDF2>=3.0.0",
        "pydantic>=2.10.5",
        "pydantic-settings>=2.2.1",
        "pyttsx3>=2.98",
        "questionary>=2.0.1",
        "rich>=13.9.4",
        "typer>=0.13.1",
        "voyageai>=0.3.0",
        "numpy>=1.26.0",
        "uv>=0.1.0",
        "pyyaml>=6.0.0",
        "realtimestt>=0.3.93",
        "realtimetts[system]==0.4.40"
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.3",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest-asyncio>=0.23.0",
            "types-pydantic>=2.10.2",
            "types-httpx>=0.27.0"
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
            "tarotai-cleanup=scripts.dev.cleanup:main",
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
