import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    

setuptools.setup(
    name="hyutils-hyutil-hoyun-lab",
    version="0.0.8.3",
    url="https://www.hoyun.co.kr",
    license="MIT",
    author="nohgan im",
    author_email="fory2k@hoyun.co.kr",
    description="Hoyun Lab Python Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/schooldevops/python-tutorials/issues",
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