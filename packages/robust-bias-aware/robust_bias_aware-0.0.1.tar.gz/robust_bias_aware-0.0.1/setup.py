import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robust_bias_aware",
    version="0.0.1",
    author="S. Sarkar",
    author_email="suryadipto.sarkar@fau.de",
    description="A python package for ROBUST disease module mining algorithm with study bias correction via the incorporation of bias-aware edge costs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wino6687/pip_conda_demo",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)
