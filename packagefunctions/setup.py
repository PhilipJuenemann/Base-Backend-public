from setuptools import setup
from setuptools import find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
    requirements = [x.strip() for x in content]

setup(name='packagefunctions', # To find the package name within the folder
      description="The Base - LeWagon", # Whatever you want
      packages=find_packages(),
      install_requires=requirements) # To list the necessary libraries
