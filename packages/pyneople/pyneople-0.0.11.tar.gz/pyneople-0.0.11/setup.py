import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyneople",
    version="0.0.11",
    author="ippo252525",
    author_email="ippo252525@gmail.com",
    description="Neople Open API wrapper for data analyst",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ippo252525/PyNeople",
    project_urls={
        "Bug Tracker": 'https://github.com/ippo252525/PyNeople/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)