import setuptools
import os        

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "1.1.14"

if os.environ.get('TARGET_ENV'):
    __version__ = __version__ + ".dev" + os.environ['CI_JOB_ID']

setuptools.setup(
    name="improutils",
    author="ImproLab",
    version=__version__,
    author_email="improlab@fit.cvut.cz",
    description="Package with useful functions for BI-SVZ coursework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ImprolabFIT/improutils_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.19.3",
        "Pillow>=8.1.0",
        "matplotlib>=3.4.2",
        "opencv-python>=4.5.3.56",
        "Pylon>=0.4.4",
        "pytesseract>=0.3.7",
        "wheel",
        "natsort>=5.3.3",
        "PyYAML>=5.3.1",
        "qreader>=3.11",
      ],
    python_requires='>=3.6',
)
