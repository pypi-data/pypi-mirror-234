from setuptools import setup, find_packages

with open("vectorshift/requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="vectorshift",
    version="0.0.12",
    packages=find_packages(),
    author="Alex Leonardi, Eric Shen",
    author_email="support@vectorshift.ai",
    description="VectorShift Python SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
