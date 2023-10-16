import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup (
    name="githubapi4research",
    version='0.0.2',
    author="nixianjun6",
    author_email="18373052@buaa.edu.cn",
    description="easier to use github api for research",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/nixianjun6/githubapi4research",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)