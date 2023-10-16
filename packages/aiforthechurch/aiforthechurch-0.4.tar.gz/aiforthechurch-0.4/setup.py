from setuptools import setup, find_packages

setup(
    name="aiforthechurch",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "langdetect",
        "torch>=2.0.1",
        "peft>=0.5.0",
        "transformers>=4.34.0",
        "accelerate==0.23.0",
        "bitsandbytes>=0.41.1",
    ],
    author="Andrew Rogers, Thomas Rialan",
    author_email="andrew@biblechat.ai",
    description="Package for training and deploying doctrinally correct LLMs.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trialan/aiforthechurch",
)
