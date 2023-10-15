from setuptools import setup, find_packages

setup(
    name="aiforthechurch",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "transformers==4.34.0",
        "peft==0.5.0",
        "bitsandbytes==0.41.1",
        "accelerate==0.23.0",
    ],
    author="Thomas Rialan and Andrew Rogers",
    author_email="thomasrialan@gmail.com",
    description="Package for fine-tuning doctrinally correct LLMs.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tr416/aiforthechurch",
)
