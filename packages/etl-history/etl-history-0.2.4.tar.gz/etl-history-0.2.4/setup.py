from setuptools import setup, find_packages

# Read the contents of your README.md file for the long description
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="etl-history",
    version="0.2.4",
    description="A Python package for ETL history management",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type
    author="Nilesh Sukhwani",
    # author_email="your.email@example.com",
    # url="https://github.com/yourusername/etl-history",
    packages=find_packages(),
    install_requires=[
        "openpyxl",
        "pandas",
        "psycopg2-binary",
        "pymysql",
        "sqlalchemy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
