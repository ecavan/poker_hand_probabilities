from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'poker_hand_probabilities'
LONG_DESCRIPTION = 'A Python Package for Poker Statistics'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pokerprobs", 
        version=VERSION,
        author="Elijah Cavan",
        author_email="eli_cavan@live.ca",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)