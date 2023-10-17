from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Python package for analysis of slide-seq data on heart tissue'
LONG_DESCRIPTION = 'A package created for the complete analysis done in a heart tissue slide-seq spatial transcriptomics project.'

# Setting up
setup(
    # the name must match the folder name 'HumanHeartSpatial'
    name="HumanSpatialHeart",
    version=VERSION,
    author="Mercedes Dalman",
    author_email="meraljopedal@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'scanpy', 'seaborn', 'matplotlib', 'numpy'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'spatial transcriptomics', 'slide-seq', 'heart tissue', 'human heart'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)