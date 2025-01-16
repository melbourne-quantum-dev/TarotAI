from setuptools import setup, find_packages

setup(
    name="tarotai",
    version="0.1.0",
    description="Neural-Enhanced Tarot Reading Interface",
    author="melbourne__quantum__dev",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "anthropic==0.42.0",
        "rich==13.9.4",
        "typer==0.15.1",
        "questionary==2.1.0",
        "python-dotenv==1.0.1",
        "typing-extensions==4.12.2",
        "pydantic>=2.5.0",
    ],
    extras_require={
        'dev': [
            'pytest==8.3.4',
            'pytest-cov==6.0.0',
            'black==24.10.0',
            'flake8==7.1.1',
            "voyageai>=0.3.2",
            "transformers>=4.38.1",
            "torch>=2.2.0",
            "numpy>=1.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tarot=tarotai.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
    ],
    include_package_data=True,
    package_data={
        "tarotai": ["data/*.json"],
    },
)from setuptools import setup

setup()
