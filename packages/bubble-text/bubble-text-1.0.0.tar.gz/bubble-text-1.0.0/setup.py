from setuptools import setup

long_description = open("README.md").read()

setup(
    name="bubble-text",
    version="1.0.0",
    author="Tom Draper",
    author_email="tomjdraper1@gmail.com",
    license="MIT",
    description="Styling for colorful bubble text in the command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tom-draper/bubble-text",
    key_words="cli text styling",
    install_requires=['termcolor'],
    packages=["bubble_text"],
    python_requires=">=3.6",
)