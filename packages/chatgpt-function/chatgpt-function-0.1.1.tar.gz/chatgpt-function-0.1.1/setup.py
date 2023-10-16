from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="chatgpt-function",
    version="0.1.1",
    description="Wrapper for creating ChatGPT callable functions from docstrings",
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author="Ron Heichman",
    author_email="ronheichman@gmail.com",
    url="https://github.com/rrhd/chatgpt_function",
    packages=["chatgpt_function"],
    install_requires=[
        "docstring-parser",
    ],
)