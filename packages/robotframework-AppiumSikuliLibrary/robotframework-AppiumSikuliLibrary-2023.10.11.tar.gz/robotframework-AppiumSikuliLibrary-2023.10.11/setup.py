from setuptools import setup
from os.path import abspath, dirname, join

# Read the version from the version.py file
with open(join(dirname(abspath(__file__)), 'target', 'src', 'AppiumSikuliLibrary', 'version.py')) as f:
      exec(f.read())

DESCRIPTION = """
Appium Sikuli
=============

Getting Started
===============

**Appium - Sikuli Robot Framework Library** provides keywords for Robot Framework to test UI through Sikuli.

Support: Mobile, PC

Notes:
    `AppiumSikuliLibrary.jar` file is OS dependent. The version for Windows 64bit is included.
    If the target OS is not Windows, please get the source code from [GitHub](https://github.com), and use Maven to build `AppiumSikuliLibrary.jar` on the target OS, and replace the JAR file in the 'lib' folder.

Available Keywords
==================

Here is a list of the available keywords: [AppiumSikuliLibrary Keywords](https://thinhdnn.github.io/robotframework-AppiumSikuliLibrary/doc/AppiumSikuliLibrary.html)

Recommended Environment
=======================
- Java 11
- Python 3.10.x
"""

CLASSIFIERS = [
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Java",
      "Topic :: Software Development :: Testing",
]

setup(
      name='robotframework-AppiumSikuliLibrary',
      version=VERSION,
      description='Appium - Sikuli library for Robot Framework',
      long_description=DESCRIPTION,
      long_description_content_type='text/markdown',  # Specify the content type
      author='Thinh Nguyen',
      author_email='nguyenvanthinh.dnn@gmail.com',
      url='https://github.com/thinhntt/robotframework-AppiumSikuliLibrary',
      license='Apache License 2.0',
      keywords='robotframework testing testautomation sikuli UI on PC, Mobile',
      platforms='any',
      classifiers=CLASSIFIERS,
      package_dir={'': 'target/src'},
      packages=['AppiumSikuliLibrary'],
      package_data={'AppiumSikuliLibrary': ['lib/*.jar']},
)