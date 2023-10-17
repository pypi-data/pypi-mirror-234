from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="vector_forge",
    version="0.0.2",
    author="Simeon Emanuilov",
    author_email="simeon.emanuilov@gmail.com",
    description="Easily convert individual images into feature vectors by specifying your desired model to extract meaningful representations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.vector-forge.com/",
    license="MIT",
    packages=["vector_forge"],
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "opencv-python",
        "transformers",
        "torch",
        "tensorflow",
        "Pillow",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="vector_forge image text vector keras pytorch",
)
