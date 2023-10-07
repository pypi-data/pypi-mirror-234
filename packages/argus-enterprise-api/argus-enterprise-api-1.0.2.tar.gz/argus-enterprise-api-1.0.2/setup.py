from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="argus-enterprise-api",
    version="1.0.2",
    author="Andrei Budaes-Tanaru",
    author_email="budaesandrei@gmail.com",
    description="A Python SDK for interacting with the Argus Enterprise API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/budaesandrei/argus-enterprise-api",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 1 - Planning"
    ],
    install_requires=[
        "cryptography>=41.0.4, <42.0.0",
        "PyJWT>=2.8.0, <3.0.0",
        "requests>=2.31.0, <3.0.0",
        "setuptools>=58.1.0, <59.0.0",
    ],
    python_requires=">=3.9",
)
