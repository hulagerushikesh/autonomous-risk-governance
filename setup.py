#!/usr/bin/env python3
"""
🚀 Setup configuration for Autonomous Risk Governance Multi-Agent System
"""

from setuptools import setup, find_packages
import os

# 📖 Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Autonomous Risk Governance Multi-Agent System"

# 📦 Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="autonomous-risk-governance",
    version="1.0.0",
    description="Production-ready multi-agent system for autonomous risk governance in financial services",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Rushikesh Hulage",
    author_email="rushikeshhulage@example.com",
    url="https://github.com/hulagerushikesh/autonomous-risk-governance",
    project_urls={
        "Bug Tracker": "https://github.com/hulagerushikesh/autonomous-risk-governance/issues",
        "Documentation": "https://github.com/hulagerushikesh/autonomous-risk-governance/blob/master/README.md",
        "Source Code": "https://github.com/hulagerushikesh/autonomous-risk-governance",
    },
    packages=find_packages(exclude=["tests*", "docs*"]),
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
            "locust>=2.0.0",
        ],
        "monitoring": [
            "prometheus-client>=0.17.0",
            "grafana-api>=1.0.3",
        ],
        "deployment": [
            "docker>=6.0.0",
            "kubernetes>=27.0.0",
        ],
    },
    python_requires=">=3.13",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: FastAPI",
        "Framework :: Pytest",
    ],
    keywords=[
        "risk-governance", 
        "ai", 
        "multi-agent", 
        "fastapi", 
        "banking", 
        "compliance",
        "bias-detection",
        "explainable-ai",
        "decision-support",
        "financial-services"
    ],
    entry_points={
        "console_scripts": [
            "risk-governance-api=api.main:main",
            "risk-governance-test=tests.test_main:run_tests",
        ],
    },
    zip_safe=False,
)
