# setup.py
from setuptools import setup, find_packages

setup(
    name="Bernice",
    version="0.1.0",
    description="Discord Gacha Bot",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "asyncpg>=0.29.0",
        "python-dotenv>=1.0.0",
        # Add other dependencies from requirements.txt
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "bernice=src.server.main:main",
        ],
    },
)
