from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="autogonai",
    version="0.2.1",
    description="Python connector for Autogon Public APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Mbatuegwu",
    author_email="david@autogon.ai",
    maintainer="Chiemezie Njoku",
    maintainer_email="manuel@autogon.ai",
    url="https://github.com/autogoninc/autogonai-python",
    packages=find_packages(),
    install_requires=["python-dotenv==1.0.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
