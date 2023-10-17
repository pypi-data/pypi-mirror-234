from setuptools import setup

setup(
    name="vector_forge",
    version="0.0.1",
    author="Simeon Emanuilov",
    author_email="simeon.emanuilov@gmail.com",
    description="Library to facility converting with vectors",
    long_description="Vector Forge is a Python package designed for easy transformation of various data types into feature vectors.",
    long_description_content_type="text/x-rst",
    license="MIT",
    packages=["vector_forge"],
    install_requires=[
        "numpy",
        "opencv-python",
        "transformers",
        "torch",
        "tensorflow"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="vector_forge image text vector keras pytorch",
)
