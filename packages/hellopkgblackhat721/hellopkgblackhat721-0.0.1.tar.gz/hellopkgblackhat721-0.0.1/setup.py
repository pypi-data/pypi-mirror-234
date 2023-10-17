from setuptools import setup, find_packages
import codecs

VERSION = '0.0.1'
DESCRIPTION = 'Basic hello package'

# Setting up
setup(
    name="hellopkgblackhat721",
    version=VERSION,
    author="Vivek",
    author_email="<vivekmahajan085@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
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