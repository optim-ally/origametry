import pathlib
from distutils.core import setup


HERE = pathlib.Path(__file__).parent.resolve()
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="origametry",
    version="0.0.5",
    description="Package to perform calculations using the Huzita-Justin axioms for 2-dimensional origami",
    author="Alastair Stanley",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=">=3.9.0",
    install_requires=[
        "matplotlib>=3.9.0",
        "multimethod>=1.11.2",
        "numpy>=1.26.4",
        "sympy>=1.12",
    ],
    project_urls={
        "Source": "https://github.com/optim-ally/origametry.git",
    },
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",

        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": "src"},
    include_package_data=True,
)
