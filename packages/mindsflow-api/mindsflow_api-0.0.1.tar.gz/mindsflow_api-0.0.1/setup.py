from setuptools import setup

setup(
    name="mindsflow_api",
    version="0.0.1",
    description="A Python library for mindsflow.ai api",
    author="Shawn-Tam",
    author_email="shawn@mindsflow.ai",
    packages=["mindsflow_api", "mindsflow_api.models", "mindsflow_api.utils"],
    install_requires=[
        "requests",
        "httpx",
        "redis"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # or "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
