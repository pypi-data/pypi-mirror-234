from setuptools import setup, find_packages

setup(
    name="quillsql",
    version="1.0",
    packages=find_packages(),
    install_requires=["psycopg2-binary", "requests"],
    author="Quill",
    author_email="shawn@quillsql.com",
    description="Quill SDK for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/quill-sql/quill-python",
)
