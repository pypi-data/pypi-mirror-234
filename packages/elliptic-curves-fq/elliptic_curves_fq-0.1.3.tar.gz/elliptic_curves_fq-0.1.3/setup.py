from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = 'ECC Library'
LONG_DESCRIPTION = 'A package that allows to compute in Elliptic Curves on the field F(p^n)'

# Setting up
setup(
    name="elliptic_curves_fq", 
    version=VERSION,
    author="Kaspar Hui",
    author_email="<kaspar.hui@bluewin.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    install_requires=[],
    keywords=['python', 'ECC', 'finite Fields'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)