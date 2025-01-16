from setuptools import setup, find_packages

setup(
    name="chimera-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0.0",
        "colorama>=0.4.4",
        "docker>=6.0.0",
        "rich>=13.0.0",
        "questionary>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "chimera=chimera.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Amir",
    author_email="amirofcodes@github.com",
    description="A template-based development environment manager",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Amirofcodes/ChimeraStack_CLI",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)