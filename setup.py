"""Setup configuration for biotech-research-agent"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="biotech-research-agent",
    version="0.1.0",
    author="junweima-1234",
    description="Autonomous Buy-Side Biotech Fundamental Research Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junweima-1234/biotech-research-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-google-genai>=0.0.5",
        "pydantic>=2.0",
        "python-dotenv>=1.0",
        "tavily-python>=0.1",
        "click>=8.0",
        "aiohttp>=3.8",
        "requests>=2.28",
    ],
    entry_points={
        "console_scripts": [
            "biotech-agent=biotech_agent.cli:cli",
        ],
    },
)
