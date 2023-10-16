from setuptools import find_packages, setup

setup(
    name="korbit-mentor",
    version="3.6.6",
    packages=find_packages(),
    long_description=open("PUBLIC_README.md").read(),
    long_description_content_type="text/markdown",
    description="Korbit mentor CLI tool will allow you to analyze any local files.",
    author="Korbit Technologies Inc.",
    author_email="team@korbit.ai",
    url="https://www.korbit.ai",
    keywords=["SOFTWARE", "DEVELOPMENT", "MENTOR", "ENGINEER"],
    install_requires=["validators", "beautifulsoup4", "click", "rich", "requests", "gitpython"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "korbit = korbit.cli:cli",  # Define the entry point for your CLI
        ],
    },
)
