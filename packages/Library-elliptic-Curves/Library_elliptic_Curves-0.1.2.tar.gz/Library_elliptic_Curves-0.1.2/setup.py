from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'ECC Library'
LONG_DESCRIPTION = 'A package that allows to compute in Elliptic Curves on the field F(p^n)'

# Setting up
setup(
    name="Library_elliptic_Curves", 
    version=VERSION,
    author="Kaspar Hui",
    author_email="<kaspar.hui@bluewin.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)