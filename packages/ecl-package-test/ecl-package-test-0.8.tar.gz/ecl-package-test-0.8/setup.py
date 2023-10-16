import setuptools

setuptools.setup(
    name="ecl-package-test",
    version="0.08",
    license="MIT",
    author="Earth Coding Lab",
    author_email="syw5141@gmail.com",
    description="ecl package TBA",
    url="https://github.com/EarthCodingLab/ecl-package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["ecl-package = package.main:main"]},
    scripts=["bin/package.cmd"],
)
