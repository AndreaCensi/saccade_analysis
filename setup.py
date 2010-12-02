from setuptools import setup
from setup_info import scripts, console_scripts

setup(
    name='saccade_analysis',
	version="1.0",
    package_dir={'':'src-python'},
    packages=['saccade_analysis'],
    install_requires=['geometric_saccade_detector', 'matplotlib',
                      'reprep'],
    entry_points={ 'console_scripts': console_scripts},
      
    author="Andrea Censi",
    author_email="andrea@cds.caltech.edu",
    description="This package provides utils to analyze saccade data.",
    license="GPL"
)

