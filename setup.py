from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function returns a list of requirements from the given file path.
    """
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .') # remove -e . if present
    return requirements


setup(
    name='DiamondPricePrediction',
    version='0.0.1',
    author='Atharv Prashant Tungatkar',
    author_email='atharvpt52@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()

)