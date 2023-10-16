from setuptools import setup
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='yolosplitter',
    version='0.4.4',
    description="Tool to Create,Modify YOLO dataset and much more...",
    author= 'wpnx',
    url = 'https://github.com/sandeshkharat87/yolo-splitter',
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['yolo splitter', "split datasets", 'yolo split','yolos split dataset','yolo','yolosplitter','yolo-splitter'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['yolosplitter'],
    package_dir={'':'src'},
    install_requires = [
        'pandas',
        'tqdm',
        'PyYAML'
    ]
)
