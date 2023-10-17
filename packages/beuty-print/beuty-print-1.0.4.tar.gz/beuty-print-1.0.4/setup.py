from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.4'
DESCRIPTION = 'Just a simple library to print your script outputs in more neat / colorful way without much overhead'
LONG_DESCRIPTION = 'Library used to display your prints in colors and more structurized using ansi color codes, it is simple library without much garbage on it'

# Setting up
setup(
    name="beuty-print",
    version=VERSION,
    author="Hex24 (Markas Vielavičius)",
    author_email="<markas.vielavicius@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,   
    install_requires=["colorama"],
    keywords=['python', 'printer', 'print', 'color', 'simple', 'format'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
    # entry_points={
    #     'console_scripts': [
    #         'beutyprint=ProxyRipper.ProxyRipper:main',
    #     ],
    # }
)
