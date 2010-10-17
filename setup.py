from setuptools import setup

setup(
    name='saccade_analysis',
	version="1.0",
    package_dir={'':'src-python'},
    py_modules=['saccade_analysis'],
    install_requires=['geometric_saccade_detector', 'matplotlib'],
    entry_points={
         'console_scripts': [
           'sac_plot_xy  = saccade_analysis.hollywood.plot_xy_direction:main',
           'sac_sequence_analysis = saccade_analysis.analysis201009.sequence_analysis:main',
           'sac_levy_analysis = saccade_analysis.analysis201009.levy_analysis:main',
           'sac_tammero_analysis = saccade_analysis.tammero.tammero_analysis:main',
        ]
      },
      
    
    author="Andrea Censi",
    author_email="andrea@cds.caltech.edu",
    description="This package provides utils to analyse saccade data.",
    license="GPL"
)


