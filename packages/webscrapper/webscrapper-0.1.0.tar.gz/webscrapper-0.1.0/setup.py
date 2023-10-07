import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webscrapper",
    version="0.1.0",
    author="webii",
    author_email="webii@pm.me",
    description="Simple client for Web scrapper API https://scrapper.scurra.space/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pi11/webscrapper-client-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
