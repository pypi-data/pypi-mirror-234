from setuptools import setup

setup(
    name="chatgpt-function",
    version="0.1.0",
    description="Wrapper for creating ChatGPT callable functions from docstrings",
    author="Ron Heichman",
    author_email="ronheichman@gmail.com",
    url="https://github.com/rrhd/chatgpt_function",
    packages=["chatgpt_function"],
    install_requires=[
        "docstring-parser",
    ],
)
